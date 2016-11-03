import numpy as np
import subprocess
import os
from shutil import copyfile

PROJECT_DIR = "../" #ror-dam-simulation directory
CE_QUAL_W2_EXE = "../../bin/w2_ivf32_v372.exe"
CONTROL_DIR = PROJECT_DIR + "model-control-chain/"
TOKENIZED_CON_FILE = "w2_con_tokenized.npt"
CON_FILE = "w2_con.npt"
TEMPERATURE_FILE = "spr.opt"
QWO_FILE = "qwo_34.opt"
QOUT_FILE = "qot_br1.npt"
RSI_FILE = "rso%STEP%.opt"
CHAINING_FILE = CONTROL_DIR + "scripts/propagate.flow.sh"

#TODO: Remove these parameters from the control file
def modifyControlFile(fileDir, timeStart, timeEnd, year):
    with open(fileDir + CON_FILE, "w") as fout:
        with open(fileDir + "inputs/control/" + TOKENIZED_CON_FILE, "r") as fin:
            for line in fin:
                line = line.replace("%RSIFN%", RSI_FILE.replace("%STEP%", str(timeStart)))
                line = line.replace("%QINFN%", "qin.npt")
                line = line.replace("%TINFN%", "tin.npt")
                line = line.replace("%METFN%", "met.npt")
                line = line.replace("%TMSTRT%", str(timeStart).rjust(8))
                line = line.replace("%TMEND_%", str(timeStart + timeStep).rjust(8))
                line = line.replace("%YEAR__%", str(year).rjust(8))
                fout.write(line)

def setAction(fileDir, timeStart, gatesOn, wb):
    line = str(timeStart+1).rjust(8)
    line += str( 1000 if gatesOn[wb][0] else 0 ).rjust(8) #TODO: How much output for "on"
    line += str( 1000 if gatesOn[wb][1] else 0 ).rjust(8)
    line += "\n"
    with open(fileDir + QOUT_FILE, "a") as f:
        f.write(line)

def getReward(fileDir, gatesOn):
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

def copyInYearFiles(year, numDams):
    copyfile( CONTROL_DIR + "wb1/inputs/QIN" + str(year) +".npt", CONTROL_DIR + "wb1/qin.npt")
    copyfile( CONTROL_DIR + "wb1/inputs/TIN" + str(year) +".npt", CONTROL_DIR + "wb1/tin.npt")
    for wb in range(1, numDams + 1):
        copyfile( CONTROL_DIR + "wb" + str(wb) + "/inputs/met" + str(year) +".npt", CONTROL_DIR + "wb" + str(wb) + "/met.npt")
        spinupDir =  CONTROL_DIR + "wb" + str(wb) + "/inputs/spinup/" + str(year)
        for f in os.listdir(spinupDir):
            filename = spinupDir + "/" + f
            if os.path.isfile(filename):
                copyfile( filename , CONTROL_DIR + "wb" + str(wb) + "/" + f)

timeStart = 60
timeStep = 1
year = 2015

numDams = 4
numGates = 3 # per dam
gatesOn = np.zeros((numDams, numGates))
gatesOn[0, 0] = 1
gatesOn[0, 1] = 1
gatesOn[1, 0] = 1

copyInYearFiles(year, numDams)
for i in range(30):

    for wb in range(numDams):
        wbDir = CONTROL_DIR + "wb" + str(wb + 1) + "/"
        modifyControlFile(wbDir, timeStart, timeStart + timeStep, year)
        setAction(wbDir, timeStart, gatesOn, wb)
        path = os.getcwd()
        os.chdir(wbDir)
        subprocess.check_call(['wine', CE_QUAL_W2_EXE])
        os.chdir(path)
        if wb != (numDams - 1):
            subprocess.check_call([CHAINING_FILE, "wb" + str(wb+1), "wb" + str(wb+2)])

    outputDir = CONTROL_DIR + "wb" + str(numDams) + "/"
    #print getReward(outputDir, gatesOn)
    timeStart = timeStart + timeStep
