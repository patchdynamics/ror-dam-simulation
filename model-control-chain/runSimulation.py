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
STEP_SIZE = 0.01

# Actions
# Original
#SPILLWAY_OUTFLOWS = [0, 600, 1800]
#POWERHOUSE_OUTFLOWS = [500, 1500, 3000]
#HYPOLIMNAL_OUTFLOWS = [0, 1000]
# Simple
# POWERHOUSE_OUTFLOWS = [500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700, 2900, 3100, 3300, 3500, 3700, 3900, 4100, 4500, 5000, 5500, 6000]
# Two Way
SPILLWAY_OUTFLOWS = [500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700, 2900, 3100, 3300, 3500]
POWERHOUSE_OUTFLOWS = [500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700, 2900, 3100, 3300, 3500]
HYPOLIMNAL_OUTFLOWS = [0]

# Reward parameters
MIN_ELEVATION = 210
MAX_ELEVATION = 230
TARGET_HIGH_ELEVATION = 223.5
TARGET_LOW_ELEVATION = 222.5
TARGET_ELEVATION = 223

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
    #reward = 2 - abs(elevation - TARGET_ELEVATION)
    reward = 0
    if elevation < MIN_ELEVATION or elevation > MAX_ELEVATION:
        reward = -100

    temperatureOut = np.loadtxt( "wb" + str(wb+1) + "/two_34.opt", skiprows=3)
    temperatureOut = temperatureOut[-1,1]
    if temperatureOut > 21.2:
        reward = -100
    return reward, elevation

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

# returns state represented as a tuple of (QINs, TINs, airTempForecast, solarFluxForecast, elevations, temps)
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

    # Weather Judgement
    # Read in next week of weather
    # Average and noise it
    # this is a 'fake forecast'
    # Note: Using the same meteorological data for all dams
    futureDays = 5
    met = np.loadtxt('wb1/met.npt', skiprows=3, delimiter=',')
    future = met[np.where(np.logical_and(met[:,0] >= timeStart, met[:,0] < timeStart+futureDays))]
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
        seg34ForTime = seg34[np.where(np.floor(seg34[:,0]) == timeStart)]
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
   if not TESTING and random.random() < EPSILON_GREEDY:
        #print 'Random'
        return random.randrange(possibleActions.shape[0])
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

timeStartBegin = 60
timeStep = 1
year = 2014
numDams = 1
numDays = 215
repeat = 1
algClass = getattr(importlib.import_module("algorithms.linear"), "Linear")

if len(sys.argv) > 1:
    try:
      opts, args = getopt.getopt(sys.argv[1:],"ha:e:r:d:ts:",["eps=", "alg=", "repeat=", "dams=", "days=", "test", "year=", "step="])
    except getopt.GetoptError:
      print 'runSimulation.py -a <algorithm> -r <repeat> -e <epsilon> -d <dams>, days=<days> -s <stepsize> --test'
      sys.exit()

    for opt, arg in opts:
      if opt == '-h':
         print 'runSimulation.py -r <repeat> -e <epsilon> -d <numDams>, --days <numDays> -s <stepsize> --test'
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
      elif opt in ("-a", "--alg"):
          algClass = getattr(importlib.import_module("algorithms."+arg.lower()), arg)

possibleActions = calculatePossibleActions()
#_print possibleActions
algorithm = algClass(numDams, STEP_SIZE, FUTURE_DISCOUNT, possibleActions)
for r in range(repeat):
    timeStart = timeStartBegin
    copyInYearFiles(year, numDams)
    state = getState(timeStart, year, np.ones(numDams)*4, possibleActions.shape[0])

    algorithm.loadModel(state)

    actionInds = np.zeros(numDams)
    rewards = np.zeros(numDams)
    elevations = np.zeros(numDams)
    for i in range(numDays):
        print 'Day ' + str(timeStart)
        for wb in range(numDams):
            actionInd = getAction(state, wb, possibleActions)
            actionInds[wb] = actionInd
            action = possibleActions[actionInd]
            wbDir = 'wb'+str(wb+1)+'/'
            ##_print wbDir
            modifyControlFile(wbDir, timeStart, timeStart + timeStep, year)
            setAction(wbDir, timeStart, action, wb)
            path = os.getcwd()
            os.chdir(wbDir)
            subprocess.check_call(['../../bin/cequalw2.v371.mac.fast', '.'], shell=True)
            os.chdir(path)
            if wb != (numDams - 1):
                subprocess.check_call([CHAINING_FILE, "wb" + str(wb+1), "wb" + str(wb+2)])

            rewards[wb], elevations[wb] = getReward(wb)
            #raw_input("Press Enter to continue...")

        nextState = getState(timeStart + timeStep, year, actionInds, possibleActions.shape[0])
        if not TESTING:
            algorithm.incorporateObservations(state, actionInds, rewards, nextState)

        (wbQIN, wbTIN, airTempForecast, solarFluxForecast, elevations, temps) = nextState
        outputStats(rewards, elevations, wbQIN, actionInds, possibleActions)

        if True in (rewards < 0):
            # Move to next epoch
            print 'Day ' + str(timeStart)
            print 'Lose'
            algorithm.saveModel()
            sys.exit()


        timeStart = timeStart + timeStep
        state = nextState



    algorithm.saveModel()
