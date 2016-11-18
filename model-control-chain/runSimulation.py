#!/usr/bin/python
import numpy as np
import subprocess
import os
from shutil import copyfile
import struct
from sklearn.utils.extmath import cartesian
import random
import re
import sys, getopt

PROJECT_DIR = "../" #ror-dam-simulation directory
CE_QUAL_W2_EXE = "../bin/cequalw2.v371.mac"
CONTROL_DIR = PROJECT_DIR + "model-control-chain/"
TOKENIZED_CON_FILE = "w2_con_tokenized.npt"
CON_FILE = "w2_con.npt"
TEMPERATURE_FILE = "spr.opt"
QWO_FILE = "qwo_34.opt"
QOUT_FILE = "qot_br1.npt"
RSI_FILE = "rso%STEP%.opt"
CHAINING_FILE = CONTROL_DIR + "scripts/propagate.flow.sh"
ELEVATION_FILE = "wl.opt"
STATS_DIR = "stats/"
WEIGHTS_FILE = "weights.npy"
REWARDS_FILE = "rewards.txt"
ACTIONS_FILE = "actions.txt"
QIN_FILE = "QINs.txt"

# Hyperparameters
EPSILON_GREEDY = 0.25 # TODO: Should start high & decrease over time
FUTURE_DISCOUNT = 0.75
STEP_SIZE = 0.01

# Actions
#SPILLWAY_OUTFLOWS = [0, 600, 1800]
#POWERHOUSE_OUTFLOWS = [500, 1500, 3000]
#HYPOLIMNAL_OUTFLOWS = [0, 1000]
SPILLWAY_OUTFLOWS = [0]
POWERHOUSE_OUTFLOWS = [500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700, 2900, 3100, 3300, 3500, 3700, 3900, 4100, 4500, 5000, 5500, 6000]
HYPOLIMNAL_OUTFLOWS = [0]

# Reward parameters
MIN_ELEVATION = 220
MAX_ELEVATION = 225
TARGET_HIGH_ELEVATION = 223.5
TARGET_LOW_ELEVATION = 221.5

# Set to true to stop learning
TESTING = False

def modifyControlFile(fileDir, timeStart, timeEnd, year):
    with open(fileDir + CON_FILE, "w") as fout:
        with open(fileDir + "inputs/control/" + TOKENIZED_CON_FILE, "r") as fin:
            for line in fin:
                line = line.replace("%RSIFN%", RSI_FILE.replace("%STEP%", str(timeStart)))
                line = line.replace("%TMSTRT%", str(timeStart).rjust(8))
                line = line.replace("%TMEND_%", str(timeEnd).rjust(8))
                line = line.replace("%YEAR__%", str(year).rjust(8))
                fout.write(line)

def setAction(fileDir, timeStart, action, wb):
    line = str(timeStart+1).rjust(8)
    line += str(action[0]).rjust(8)
    line += str(action[1]).rjust(8)
    line += str(action[2]).rjust(8)
    line += "\n"
    with open(fileDir + QOUT_FILE, "a") as f:
        f.write(line)

def getReward(wb):
    wlFile = CONTROL_DIR + "wb" + str(wb+1) + "/" + ELEVATION_FILE
    elevations = np.genfromtxt(wlFile, delimiter=",")
    elevation = elevations[-1,33]
    if elevation < MIN_ELEVATION:
        #reward =  -np.exp(MIN_ELEVATION - elevation)
        reward = -5
    elif elevation < TARGET_LOW_ELEVATION:
        reward = -1
    elif elevation > MAX_ELEVATION:
        #reward = -np.exp(elevation - MAX_ELEVATION)
        reward = -5
    elif elevation > TARGET_HIGH_ELEVATION:
        reward = -1
    else:
        reward = 2
    return reward, elevation


'''
    temps = np.genfromtxt(fileDir + TEMPERATURE_FILE, delimiter=",", skip_header=1, usecols = 4)
    # TODO: This is for one dam, do the same for other dams
    if gatesOn[0,1]:
        powerStr = int(np.sum(gatesOn[0,:2]))
        print powerStr
        qPowerGate = np.genfromtxt(fileDir + QWO_FILE, delimiter=",", skip_header=3, usecols=(1+powerStr))
    else:
        qPowerGate = 0
    print temps
    print qPowerGate
    return qPowerGate - np.mean(temps) #TODO: Calculate a reward
'''

def copyInYearFiles(year, numDams):
    for wb in range(1, numDams + 1):
        copyfile( CONTROL_DIR + "wb" + str(wb) + "/inputs/met" + str(year) +".npt", CONTROL_DIR + "wb" + str(wb) + "/met.npt")
        spinupDir =  CONTROL_DIR + "wb" + str(wb) + "/inputs/spinup/" + str(year)
        for f in os.listdir(spinupDir):
            filename = spinupDir + "/" + f
            if os.path.isfile(filename):
                copyfile( filename , CONTROL_DIR + "wb" + str(wb) + "/" + f)
    #copyfile( CONTROL_DIR + "wb1/inputs/QIN.CONSTANT.npt", CONTROL_DIR + "wb1/qin.npt")
    copyfile( CONTROL_DIR + "wb1/inputs/QIN" + str(year) +".npt", CONTROL_DIR + "wb1/qin.npt")
    copyfile( CONTROL_DIR + "wb1/inputs/TIN" + str(year) +".npt", CONTROL_DIR + "wb1/tin.npt")

def calculatePossibleActions():
    return cartesian((SPILLWAY_OUTFLOWS, POWERHOUSE_OUTFLOWS, HYPOLIMNAL_OUTFLOWS))

def getState(timeStart, year, actionInds, numActions):
    wbQIN = np.empty(numDams)
    wbTIN = np.empty(numDams)

    # Get QIN/TIN for today on Dam 1
    wbiQIN= np.loadtxt('wb1/qin.npt', skiprows=3)
    wbQIN[0] = wbiQIN[np.where(wbiQIN[:,0]==timeStart),1]
    wbiTIN= np.loadtxt('wb1/tin.npt', skiprows=3)
    wbTIN[0] = wbiTIN[np.where(wbiTIN[:,0]==timeStart),1]

    # Read last QIN/TIN for each of Dams 2-4
    for f in range(2, numDams+1):
        wbiQIN = np.loadtxt('wb'+str(f)+'/qin.npt', skiprows=3)
        wbQIN[f-1] = wbiQIN[np.where(wbiQIN[:,0]==timeStart),1]
        wbiTIN = np.loadtxt('wb'+str(f)+'/tin.npt', skiprows=3)
        wbTIN[f-1] = wbiTIN[np.where(wbiTIN[:,0]==timeStart),1]

    wbQINindicators = np.empty([numDams,8])
    wbTINindicators = np.empty([numDams,6])
    for f in range(0, numDams):
        wbQINindicators[f,0] = int(wbQIN[f] <= 700)
        wbQINindicators[f,1] = int(wbQIN[f] > 700  and wbQIN[f] < 1200)
        wbQINindicators[f,2] = int(wbQIN[f] > 1200  and wbQIN[f] < 1700)
        wbQINindicators[f,3] = int(wbQIN[f] > 1700  and wbQIN[f] < 2200)
        wbQINindicators[f,4] = int(wbQIN[f] > 2200  and wbQIN[f] < 2700)
        wbQINindicators[f,5] = int(wbQIN[f] > 2700  and wbQIN[f] < 3200)
        wbQINindicators[f,6] = int(wbQIN[f] > 3700  and wbQIN[f] < 4200)
        wbQINindicators[f,7] = int(wbQIN[f] > 4200)
        wbTINindicators[f,0] = int(wbTIN[f] <= 12)
        wbTINindicators[f,1] = int(wbTIN[f] > 12 and wbTIN[f] <= 14)
        wbTINindicators[f,2] = int(wbTIN[f] > 14 and wbTIN[f] <= 16)
        wbTINindicators[f,3] = int(wbTIN[f] > 16 and wbTIN[f] <= 18)
        wbTINindicators[f,4] = int(wbTIN[f] > 18 and wbTIN[f] <= 20)
        wbTINindicators[f,5] = int(wbTIN[f] > 20)
    #print(wbQINindicators)
    #print(wbTINindicators)

    # Weather Judgement
    # Read in next week of weather
    # Average and noise it
    # this is a 'fake forecast', and we will only use the first one for now
    weatherJudgements = np.empty([numDams,2])
    futureDays = 5
    for f in range(1, numDams+1):
        met = np.loadtxt('wb'+str(f)+'/met.npt', skiprows=3, delimiter=',')
        future = met[np.where(np.logical_and(met[:,0] >= timeStart, met[:,0] < timeStart+futureDays))]
        average = sum(future)/futureDays
        airTempForecast = np.random.normal(average[1], scale=2)
        airTempJudgement = int(airTempForecast > 65)
        solarFluxForecast = np.random.normal(average[6], scale=50)
        solarFluxJudgement = int(solarFluxForecast > 300)
        weatherJudgements[f-1] = [airTempJudgement, solarFluxJudgement]

    elevationJudgements = np.empty([numDams,5])
    temperatureJudgements = np.empty([numDams,3])
    for f in range(1, numDams+1):
        # Water Level
        wlFile = CONTROL_DIR + "wb" + str(f) + "/" + ELEVATION_FILE
        elevations = np.genfromtxt(wlFile, delimiter=",")
        elevation = elevations[-1,33]
        elevationHigh = int(elevation > MAX_ELEVATION)
        elevationLow = int(elevation < MIN_ELEVATION)
        elevationTargetHigh = int(not elevationHigh and (elevation >= TARGET_HIGH_ELEVATION))
        elevationTargetLow = int(not elevationLow and (elevation <= TARGET_LOW_ELEVATION))
        elevationOK = int(elevation < TARGET_HIGH_ELEVATION and elevation > TARGET_LOW_ELEVATION)
        elevationJudgements[f-1] = [elevationHigh, elevationLow, elevationTargetHigh, elevationTargetLow, elevationOK]

        # Output Structure +/- 65 F / 16 C
        seg34 = np.loadtxt('wb'+str(f)+'/spr.opt', skiprows=3, usecols=[1,4])
        seg34ForTime = seg34[np.where(np.floor(seg34[:,0]) == timeStart)]
        #temp220 = int(seg34ForTime[seg34ForTime[:,0].size - 15,1] > 65)
        #temp202 = int(seg34ForTime[seg34ForTime[:,0].size - 11,1] > 65)
        #temp191 = int(seg34ForTime[seg34ForTime[:,0].size - 6,1] > 65)
        temp220 = 0
        temp202 = 0
        temp191 = 0
        temperatureJudgements[f-1] = [temp220, temp202, temp191]

    # Construct State Array
    stateArray = elevationJudgements.flatten()
#    stateArray = np.append(stateArray, weatherJudgements[0,0])
#    stateArray = np.append(stateArray, temperatureJudgements.flatten())
    stateArray = np.append(stateArray, wbQINindicators)
#    stateArray = np.append(stateArray, wbTINindicators)

    gateState = np.zeros((numDams, numActions)) #numDams x numActions
    for i in range(numDams):
        gateState[i, actionInds.astype(int)[i]] = 1

#    stateArray = np.append(stateArray, gateState.flatten())

    return stateArray, wbQIN

def getAction(state, weights, possibleActions):
   if not TESTING and random.random() < EPSILON_GREEDY:
        return random.randrange(possibleActions.shape[0])
   else:
        [bestActionInd, Vopt] = getBestAction(state, weights, possibleActions)
        return bestActionInd

def getBestAction(state, weights, possibleActions):
    Qopts = np.empty(possibleActions.shape[0])
    for actionInd in range(possibleActions.shape[0]):
        Qopts[actionInd] = calculateQopt(state, actionInd, weights)
    print 'Qopts'
    print Qopts
    bestActionIndices = np.argwhere(Qopts == np.max(Qopts))
    bestActionInd = random.choice(bestActionIndices)[0] # Make sure not always choosing first action if all valued same
    return bestActionInd, Qopts[bestActionInd]

def getFeatures(state, actionInd, shape):
    features = np.zeros(shape)
    features[:, actionInd] = state # TODO: Add a bias term?
    return features

def calculateQopt(state, actionInd, weights):
    features = getFeatures(state, actionInd, weights.shape)
    return weights.flatten().dot(features.flatten())

# TODO: Add regularization?
def updateWeights(state, actionInds, rewards, nextState, weights, possibleActions):
    print 'state'
    print state
    print 'next state'
    print nextState
    print 'rewards'
    print rewards
    print 'actionInds'
    print actionInds
    print 'weights'
    print weights
    for i in range(numDams):
        features = getFeatures(state, actionInds[i], weights[i].shape)
        print 'features'
        print features
        [nextAction, Vopt] = getBestAction(nextState, weights[i], possibleActions)
        error = calculateQopt(state, actionInds[i], weights[i]) - (rewards[i] + FUTURE_DISCOUNT * Vopt)
        print 'Qopt   Vopt'
        print str(calculateQopt(state, actionInds[i], weights[i])) + '    ' + str(Vopt)
        weights[i] = weights[i] - STEP_SIZE * error * features
    print 'updated weights'
    print weights
    return weights

def outputStats(weights, rewards, elevations, wbQIN, actionInds, possibleActions):
    with open(STATS_DIR + REWARDS_FILE, "a") as fout:
        np.savetxt(fout, rewards, newline=",")
        np.savetxt(fout, elevations, newline=",")
        fout.write("\n")
    with open(STATS_DIR + ACTIONS_FILE, "a") as fout:
        for i in range(numDams):
            action = possibleActions[actionInds[i]]
            print action, sum(int(flow) for flow in action)
            fout.write(str(sum(int(flow) for flow in action)) + ",")
        fout.write("\n")
    with open(STATS_DIR + QIN_FILE, "a") as fout:
        np.savetxt(fout, wbQIN, newline=",")
        fout.write("\n")
    for i in range(numDams):
        weightsFile = STATS_DIR + "weights" + str(i+1) +".txt"
        with open(weightsFile, "a") as fout:
            np.savetxt(fout, weights[i].flatten(), newline=",")
            fout.write("\n")

timeStartBegin = 60
timeStep = 1
year = 2014
numDams = 4
numDays = 215
repeat = 1

if len(sys.argv) > 1:
    try:
      opts, args = getopt.getopt(sys.argv[1:],"he:r:d:t",["eps=", "repeat=", "dams=", "days=", "test", "year="])
    except getopt.GetoptError:
      print 'runSimulation.py -r <repeat> -e <epsilon> -d <dams>, days=<days> --test'
      sys.exit()

    for opt, arg in opts:
      if opt == '-h':
         print 'runSimulation.py -r <repeat> -e <epsilon> -d <numDams>, --days <numDays> --test'
         sys.exit()
      elif opt in ("-e", "--eps"):
         EPSILON_GREEDY = float(arg)
      elif opt in ("-r", "--repeat"):
         repeat = int(arg)
      elif opt in ("-d", "--dams"):
         numDams = int(arg)
      elif opt in ("--days"):
         numDays = int(arg)
      elif opt in ("--year"):
         year = int(arg)
      elif opt in ("-t", "--test"):
          TESTING = True

for r in range(repeat):
    timeStart = timeStartBegin
    copyInYearFiles(year, numDams)
    possibleActions = calculatePossibleActions()
    print possibleActions
    state, wbQIN = getState(timeStart, year, np.ones(numDams)*4, possibleActions.shape[0])

    try:
        weights = np.load(WEIGHTS_FILE)
        print "Restarting with existing weights"
    except IOError:
        weights = np.zeros((numDams, state.shape[0], possibleActions.shape[0]))
        print "Starting with new weights"

    actionInds = np.zeros(numDams)
    rewards = np.zeros(numDams)
    elevations = np.zeros(numDams)
    for i in range(numDays):
        print 'Day ' + str(timeStart)
        for wb in range(numDams):
            actionInd = getAction(state, weights[wb], possibleActions)
            actionInds[wb] = actionInd
            action = possibleActions[actionInd]
            wbDir = 'wb'+str(wb+1)+'/'
            #print wbDir
            modifyControlFile(wbDir, timeStart, timeStart + timeStep, year)
            setAction(wbDir, timeStart, action, wb)
            path = os.getcwd()
            os.chdir(wbDir)
            #subprocess.check_call(['../bin/cequalw2.v371.mac', wbDir])
            #subprocess.check_call(['scripts/run.cequalw2.sh', "wb"+str(wb+1)+'/'], shell=True)
            subprocess.check_call(['../../bin/cequalw2.v371.mac.fast', '.'], shell=True)
            #subprocess.check_call('../scripts/run.sh', shell=True)
            os.chdir(path)
            if wb != (numDams - 1):
                subprocess.check_call([CHAINING_FILE, "wb" + str(wb+1), "wb" + str(wb+2)])

            rewards[wb], elevations[wb] = getReward(wb)
            #raw_input("Press Enter to continue...")

        nextState, wbQIN = getState(timeStart + timeStep, year, actionInds, possibleActions.shape[0])
        if not TESTING:
            weights = updateWeights(state, actionInds, rewards, nextState, weights, possibleActions)

        outputStats(weights, rewards, elevations, wbQIN, actionInds, possibleActions)

        timeStart = timeStart + timeStep
        state = nextState

    np.save(WEIGHTS_FILE, weights)
