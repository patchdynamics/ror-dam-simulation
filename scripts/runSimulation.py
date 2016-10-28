import numpy as np
import subprocess
import os

CE_QUAL_W2_PATH = "/Users/ibush/Documents/Stanford/CS229/project/model/V4/executables/w2_model/"
CE_QUAL_W2_EXE = "w2_v4_32.exe"
CONTROL_DIR = "/Users/ibush/Documents/Stanford/CS229/project/ror-dam-simulation/model-control/"
TOKENIZED_CON_FILE = CONTROL_DIR + "w2_con_tokenized.npt"
CON_FILE = CONTROL_DIR + "w2_con.npt"
TEMPERATURE_FILE = CONTROL_DIR + "spr.opt"
# TODO: Correct these positions
# gateStructs in form [ktstr, kbstr, estr, wstr]
GATE_STRUCTS = np.array( [[2, 8, 220, 156],
                        [12, 23, 202, 168],
                        [20, 23, 200, 145]])

def modifyControlFile(timeStart, timeEnd, year, restart, gatesOn):
    with open(CON_FILE, "w") as fout:
        with open(TOKENIZED_CON_FILE, "r") as fin:
            for line in fin:
                line = line.replace("%QINFN%", "qin_br1.npt") #TODO: Will parameterize based on year
                line = line.replace("%TINFN%", "tin_br1.npt") #TODO: Will parameterize based on year
                line = line.replace("%METFN%", "met.npt") #TODO: Will parameterize based on year
                line = line.replace("%TMSTRT%", str(timeStart).rjust(8))
                line = line.replace("%TMEND_%", str(timeStart + timeStep).rjust(8))
                line = line.replace("%YEAR__%", str(year).rjust(8))
                rsicOn = "ON" if restart else "OFF"
                line = line.replace("%RSIC__%", rsicOn.rjust(8))
                for i in range(numDams):
                    line = line.replace("%NSTR"+str(i)+"_%", str(int(np.sum(gatesOn, 1)[i])).rjust(8))

                    ktstr = ""
                    kbstr = ""
                    estr = ""
                    wstr = ""
                    for j in range(numGates):
                        if gatesOn[i, j]:
                            ktstr += str(GATE_STRUCTS[j, 0]).rjust(8)
                            kbstr += str(GATE_STRUCTS[j, 1]).rjust(8)
                            estr += str(GATE_STRUCTS[j, 2]).rjust(8)
                            wstr += str(GATE_STRUCTS[j, 3]).rjust(8)
                    line = line.replace("%KTSTR"+str(i)+"%", ktstr)
                    line = line.replace("%KBSTR"+str(i)+"%", kbstr)
                    line = line.replace("%ESTR"+str(i)+"_%", estr)
                    line = line.replace("%WSTR"+str(i)+"_%", wstr)

                fout.write(line)

def getTemperatures():
    sprOutputs = np.genfromtxt(TEMPERATURE_FILE, delimiter=",", skip_header=1)
    return sprOutputs[:,4]


timeStart = 1
timeStep = 1
year = 2015
restart = False

numDams = 4
numGates = 3 # per dam
gatesOn = np.zeros((numDams, numGates))
gatesOn[0, 0] = 1
gatesOn[0, 1] = 1
gatesOn[1, 0] = 1

modifyControlFile(timeStart, timeStart + timeStep, year, restart, gatesOn)
path = os.getcwd()
os.chdir(CE_QUAL_W2_PATH)
subprocess.check_call(['wine', CE_QUAL_W2_EXE, CONTROL_DIR])
os.chdir(path)
print getTemperatures()
