#!/usr/bin/python
import sys, getopt
import os
sys.path.append(os.getcwd())
import numpy as np
import subprocess
from shutil import copyfile
import struct
from sklearn.utils.extmath import cartesian
import random
import re
import importlib
from algorithms.linear import Linear

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
REWARDS_FILE = "rewards.txt"
ACTIONS_FILE = "actions.txt"
QIN_FILE = "QINs.txt"

# Hyperparameters
EPSILON_GREEDY = 0.1 # TODO: Should start high & decrease over time
FUTURE_DISCOUNT = 0.75
STEP_SIZE = 0.1

# Actions
# Original
#SPILLWAY_OUTFLOWS = [0, 600, 1800]
#POWERHOUSE_OUTFLOWS = [500, 1500, 3000]
#HYPOLIMNAL_OUTFLOWS = [0, 1000]
# Simple
# POWERHOUSE_OUTFLOWS = [500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700, 2900, 3100, 3300, 3500, 3700, 3900, 4100, 4500, 5000, 5500, 6000]
# Two Way
#POWERHOUSE_OUTFLOWS = [300, 500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700, 2900, 3100, 3300, 3500]
POWERHOUSE_OUTFLOWS = [300, 500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2101, 2300, 2500, 2700, 2900, 3100, 3300, 3500]
SPILLWAY_OUTFLOWS = [0, 300, 500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2101, 2300, 2500, 2700, 2900, 3100, 3300, 3500]
HYPOLIMNAL_OUTFLOWS = [0, 300, 500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2101, 2300, 2500, 2700, 2900, 3100, 3300, 3500]
#HYPOLIMNAL_OUTFLOWS = [0, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500]

NUM_NEIGHBORS = 20
# Reward parameters
MIN_ELEVATION = 215
MAX_ELEVATION = 225
TARGET_HIGH_ELEVATION = 223.5
TARGET_LOW_ELEVATION = 222.5
TARGET_ELEVATION = 220

# Set to true to stop learning
TESTING = False
# Randomize inputs to explore the state space (mixnmatch)
RANDOMIZE = False 

def modifyControlFile(fileDir, timeStart, timeEnd, year):
    with open(fileDir + CON_FILE, "w") as fout:
        with open(fileDir + "inputs/control/" + TOKENIZED_CON_FILE, "r") as fin:
            for line in fin:
                line = line.replace("%RSIFN%", RSI_FILE.replace("%STEP%", str(timeStart)))
                line = line.replace("%TMSTRT%", str(timeStart).rjust(8))
                line = line.replace("%TMEND_%", str(timeEnd).rjust(8))
                line = line.replace("%YEAR__%", str(year).rjust(8))
                fout.write(line)

def setAction(fileDir, currentTime, action, wb):
    line = str(currentTime+1).rjust(8)
    line += str(action[0]).rjust(8)
    line += str(action[1]).rjust(8)
    line += str(action[2]).rjust(8)
    line += "\n"
    with open(fileDir + QOUT_FILE, "a") as f:
        f.write(line)

def getReward(wb, currentTime):
    wlFile = CONTROL_DIR + "wb" + str(wb+1) + "/" + ELEVATION_FILE
    elevations = np.genfromtxt(wlFile, delimiter=",")
    elevation = elevations[-1,33]
    #reward = (MAX_ELEVATION - TARGET_ELEVATION - 1) - (elevation - TARGET_ELEVATION)**2
    #if elevation < MIN_ELEVATION or elevation > MAX_ELEVATION:
    #    reward = -100

    wbiTIN= np.loadtxt('wb1/tin.npt', skiprows=3)
    tempIn = wbiTIN[np.where(wbiTIN[:,0]==currentTime),1]
    print "tempIn", tempIn

    temperatureOut = np.loadtxt( "wb" + str(wb+1) + "/two_34.opt", skiprows=3)
    temperatureOut = temperatureOut[-1,1]
    #reward = (2+tempIn - temperatureOut) # Positive reward if within 2 of tempIn
    #if temperatureOut > 16:
    #    reward = -100
    reward = 0
    if(currentTime > 100):
        reward = 15 - temperatureOut
        if(temperatureOut >= 18):
            reward = -100

    print reward
    return reward, elevation

def copyInInputFiles(year, numDams, randomize=False):
    for wb in range(1, numDams + 1):
        wbDir = CONTROL_DIR + "wb" + str(wb) + "/"
        copyfile( wbDir + "inputs/met" + str(year) +".npt", CONTROL_DIR + "wb" + str(wb) + "/met.npt")
	copyfile( wbDir + "inputs/QOUT" + str(year) +".npt", wbDir + "qot_br1.npt" )
        #subprocess.check_call(['./scripts/copy.qout.sh', '93', str(year)  ], shell=True)

    copyfile( CONTROL_DIR + "wb1/inputs/QIN" + str(year) +".npt", CONTROL_DIR + "wb1/qin.npt")
    copyfile( CONTROL_DIR + "wb1/inputs/TIN" + str(year) +".npt", CONTROL_DIR + "wb1/tin.npt")
    # here we could randomize the temperature input files if we like
    if(randomize):
        randyear = random.randint(2005,2015)
        copyfile( CONTROL_DIR + "wb1/inputs/TIN" + str(randyear) +".npt", CONTROL_DIR + "wb1/tin.npt")
        print 'rand mixnmatch ' + str(randyear)

def copyInOutputFiles(year, numDams):
    for wb in range(1, numDams + 1):
        wbDir = CONTROL_DIR + "wb" + str(wb) + "/"
        spinupDir =  wbDir + "inputs/spinup/" + str(year) + "/"
        #for f in os.listdir(spinupDir):
        #    filename = spinupDir + "/" + f
        #    if os.path.isfile(filename):
        #        copyfile( filename , CONTROL_DIR + "wb" + str(wb) + "/" + f)
        files = os.listdir(wbDir)
        for file in files:
            if file.endswith(".opt"):
                os.remove(os.path.join(wbDir,file))
        copyfile( spinupDir + "wl.opt", wbDir + "wl.opt" )
        copyfile( spinupDir + "spr.opt", wbDir + "spr.opt" )

def calculatePossibleActions():
    return cartesian((SPILLWAY_OUTFLOWS, POWERHOUSE_OUTFLOWS, HYPOLIMNAL_OUTFLOWS))

# returns state represented as a tuple of (QINs, TINs, airTempForecast, solarFluxForecast, elevations, temps)
def getState(currentTime, year, actionInds, numActions):
    wbQIN = np.empty(numDams)
    wbTIN = np.empty(numDams)

    # Get QIN/TIN for today on Dam 1
    wbiQIN= np.loadtxt('wb1/qin.npt', skiprows=3)
    wbQIN[0] = wbiQIN[np.where(wbiQIN[:,0]==currentTime),1]
    wbiTIN= np.loadtxt('wb1/tin.npt', skiprows=3)
    wbTIN[0] = wbiTIN[np.where(wbiTIN[:,0]==currentTime),1]

    # Read last QIN/TIN for each of Dams 2-4
    for f in range(2, numDams+1):
        wbiQIN = np.loadtxt('wb'+str(f)+'/qin.npt', skiprows=3)
        wbQIN[f-1] = wbiQIN[np.where(wbiQIN[:,0]==currentTime),1]
        wbiTIN = np.loadtxt('wb'+str(f)+'/tin.npt', skiprows=3)
        wbTIN[f-1] = wbiTIN[np.where(wbiTIN[:,0]==currentTime),1]

    # Weather Judgement
    # Read in next week of weather
    # Average and noise it
    # this is a 'fake forecast'
    # Note: Using the same meteorological data for all dams
    futureDays = 5
    met = np.loadtxt('wb1/met.npt', skiprows=3, delimiter=',')
    future = met[np.where(np.logical_and(met[:,0] >= currentTime, met[:,0] < currentTime+futureDays))]
    average = sum(future)/futureDays
    airTempForecast = np.random.normal(average[1], scale=2)
    solarFluxForecast = np.random.normal(average[6], scale=50)

    elevations = np.zeros(numDams)
    temps = np.zeros([numDams,3])
    for f in range(1, numDams+1):
        # Water Level
        wlFile = CONTROL_DIR + "wb" + str(f) + "/" + ELEVATION_FILE
        wbElevations = np.genfromtxt(wlFile, delimiter=",")
        elevations[f-1] = wbElevations[-1,33]

        # Output Structure +/- 65 F / 16 C
        seg34 = np.loadtxt('wb'+str(f)+'/spr.opt', skiprows=3, usecols=[1,4])
        seg34ForTime = seg34[np.where(np.floor(seg34[:,0]) == currentTime)]
        temp220 = float(seg34ForTime[seg34ForTime[:,0].size - 15,1])
        temp202 = float(seg34ForTime[seg34ForTime[:,0].size - 11,1])
        temp191 = float(seg34ForTime[seg34ForTime[:,0].size - 6,1])
        #temp220 = 0
        #temp202 = 0
        #temp191 = 0
        temps[f-1] = [temp220, temp202, temp191]

    #gateState = np.zeros((numDams, numActions)) #numDams x numActions
    #for i in range(numDams):
    #    gateState[i, actionInds.astype(int)[i]] = 1
    # stateArray = np.append(stateArray, gateState.flatten())

    return (wbQIN, wbTIN, airTempForecast, solarFluxForecast, elevations, temps)

def getAction(state, dam, possibleActions):
    (wbQIN, wbTIN, airTempForecast, solarFluxForecast, elevations, temps) = state
    actionQOUT = np.sum(possibleActions, 1)
    # Only allow actions that are 5 NN to QIN
    distances = (actionQOUT - wbQIN) ** 2
    allowedActions = np.argpartition(distances, NUM_NEIGHBORS)[:NUM_NEIGHBORS]
    #print(possibleAction[allowedActions])
    #print(np.sum(possibleActions[allowedActions],1))

    if not TESTING and random.random() < EPSILON_GREEDY:
        print 'Random'
        chosenAction = random.randrange( NUM_NEIGHBORS )
        return allowedActions[chosenAction]
    else:
        [bestActionInd, Vopt] = algorithm.getBestAction(state, dam)
        return bestActionInd

def outputStats(rewards, elevations, wbQIN, actionInds, possibleActions):
    with open(STATS_DIR + REWARDS_FILE, "a") as fout:
        np.savetxt(fout, rewards, newline=",")
        np.savetxt(fout, elevations, newline=",")
        fout.write("\n")
    with open(STATS_DIR + ACTIONS_FILE, "a") as fout:
        for i in range(numDams):
            action = possibleActions[actionInds[i]]
            #_print action, sum(int(flow) for flow in action)
            fout.write(str(sum(int(flow) for flow in action)) + ",")
        fout.write("\n")
    with open(STATS_DIR + QIN_FILE, "a") as fout:
        np.savetxt(fout, wbQIN, newline=",")
        fout.write("\n")
    for i in range(numDams):
        temperatureOut = np.loadtxt( "wb" + str(i+1) + "/two_34.opt", skiprows=3)
        temperatureOut = temperatureOut[-1,1]
        tempFile = STATS_DIR + "temperatures" + str(i+1) +".txt"
        with open(tempFile, "a") as fout:
            np.savetxt(fout, [temperatureOut], newline=",")
            fout.write("\n")
    algorithm.outputStats(STATS_DIR)

timeStart = 1
currentTimeBegin = 90
timeStep = 1
year = 2015
numDams = 1
numDays = 215 - currentTimeBegin
repeat = 1
algClass = getattr(importlib.import_module("algorithms.linear"), "Linear")

if len(sys.argv) > 1:
    try:
      opts, args = getopt.getopt(sys.argv[1:],"ha:e:r:d:ts:",["eps=", "alg=", "repeat=", "dams=", "days=", "test", "year=", "step=", "rand"])
    except getopt.GetoptError:
      print 'runSimulation.py -a <algorithm> -r <repeat> -e <epsilon> -d <dams>, days=<days> -s <stepsize> --test --rand'
      sys.exit()

    for opt, arg in opts:
      if opt == '-h':
         #_#_print 'runSimulation.py -r <repeat> -e <epsilon> -d <numDams>, --days <numDays> -s <stepsize> --test'
         sys.exit()
      elif opt in ("-e", "--eps"):
         EPSILON_GREEDY = float(arg)
      elif opt in ("-s, --step"):
         STEP_SIZE = float(arg)
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
      elif opt in ("--rand"):
          RANDOMIZE = True
      elif opt in ("-a", "--alg"):
          algClass = getattr(importlib.import_module("algorithms."+arg.lower()), arg)

possibleActions = calculatePossibleActions()
#_print possibleActions
algorithm = algClass(numDams, STEP_SIZE, FUTURE_DISCOUNT, possibleActions, NUM_NEIGHBORS)
for r in range(repeat):
    currentTime = currentTimeBegin
    if(RANDOMIZE):
        year = random.randint(2005,2015)
        print 'rand year' + str(year)
    copyInInputFiles(year, numDams, RANDOMIZE)
    copyInOutputFiles(year, numDams)
    state = getState(currentTime, year, np.ones(numDams)*4, possibleActions.shape[0])

    algorithm.loadModel(state)

    actionInds = np.zeros(numDams)
    rewards = np.zeros(numDams)
    elevations = np.zeros(numDams)
    for i in range(numDays):
        print 'Day ' + str(currentTime)
        copyInOutputFiles(year, numDams)
        for wb in range(numDams):
            actionInd = getAction(state, wb, possibleActions)
            actionInds[wb] = actionInd
            action = possibleActions[actionInd]
            wbDir = 'wb'+str(wb+1)+'/'
            ##_print wbDir
            modifyControlFile(wbDir, timeStart, currentTime + timeStep, year)
            setAction(wbDir, currentTime, action, wb)
            path = os.getcwd()
            os.chdir(wbDir)
            #subprocess.check_call(['/home/mshultz/ror-dam-simulation/bin/cequalw2.v371.linux', '.'], shell=True)
            subprocess.check_call(['../../bin/cequalw2.v371.mac.fast', '.'], shell=True)
            os.chdir(path)
            if wb != (numDams - 1):
                subprocess.check_call([CHAINING_FILE, "wb" + str(wb+1), "wb" + str(wb+2)])

            rewards[wb], elevations[wb] = getReward(wb, currentTime)
            #raw_input("Press Enter to continue...")
        #print rewards
        if True in (rewards <= -100): # Game over
            nextState = None
        else:
            nextState = getState(currentTime + timeStep, year, actionInds, possibleActions.shape[0])
        #print nextState
        if not TESTING:
            algorithm.incorporateObservations(state, actionInds, rewards, nextState)
        #print 'done with observations'
        if nextState:
            (wbQIN, wbTIN, airTempForecast, solarFluxForecast, elevationVals, temps) = nextState
            outputStats(rewards, elevations, wbQIN, actionInds, possibleActions)
        else:
            # Game over, move to next epoch
            outputStats(rewards, elevations, [0], actionInds, possibleActions)
            print 'Day ' + str(currentTime)
            print 'Lose'
            print state
            print elevations[0]
            print possibleActions[actionInds[0]]
            print np.sum(possibleActions[actionInds[0]])
            print rewards[0]
            with open(STATS_DIR + 'lastday.txt', "a") as fout:
                 np.savetxt(fout, [currentTime], newline=",")
                 fout.write("\n")
            algorithm.saveModel()
            sys.exit()

        currentTime = currentTime + timeStep
        state = nextState



    algorithm.saveModel()
    with open(STATS_DIR + 'lastday.txt', "a") as fout:
         np.savetxt(fout, [currentTime], newline=",")
         fout.write("\n")
