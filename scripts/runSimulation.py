import numpy as np

CONTROL_DIR = "../model-control/"
INPUT_CON_FILE = CONTROL_DIR + "w2_con_tokenized.npt"
OUTPUT_CON_FILE = CONTROL_DIR + "w2_con.npt"

timeStart = 1
timeStep = 1
year = 2015
restart = "OFF"

# TODO: Correct these positions
# gateStructs in form [ktstr, kbstr, estr, wstr]
gateStructs = np.array( [[2, 8, 220, 156],
                        [12, 23, 202, 168],
                        [20, 23, 200, 145]])

numDams = 4
numGates = 3 # per dam
gatesOn = np.zeros((numDams, numGates))
gatesOn[0, 0] = 1
gatesOn[0, 1] = 1
gatesOn[1, 0] = 1

with open(OUTPUT_CON_FILE, "w") as fout:
    with open(INPUT_CON_FILE, "r") as fin:
        for line in fin:
            line = line.replace("%TMSTRT%", str(timeStart).rjust(8))
            line = line.replace("%TMEND_%", str(timeStart + timeStep).rjust(8))
            line = line.replace("%YEAR__%", str(year).rjust(8))
            line = line.replace("%RSIC__%", "OFF".rjust(8))
            for i in range(numDams):
                line = line.replace("%NSTR"+str(i)+"_%", str(int(np.sum(gatesOn, 1)[i])).rjust(8))

                ktstr = ""
                kbstr = ""
                estr = ""
                wstr = ""
                for j in range(numGates):
                    if gatesOn[i, j]:
                        ktstr += str(gateStructs[j, 0]).rjust(8)
                        kbstr += str(gateStructs[j, 1]).rjust(8)
                        estr += str(gateStructs[j, 2]).rjust(8)
                        wstr += str(gateStructs[j, 3]).rjust(8)
                line = line.replace("%KTSTR"+str(i)+"%", ktstr)
                line = line.replace("%KBSTR"+str(i)+"%", kbstr)
                line = line.replace("%ESTR"+str(i)+"_%", estr)
                line = line.replace("%WSTR"+str(i)+"_%", wstr)

            fout.write(line)
