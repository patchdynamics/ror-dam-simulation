import numpy as np


MIN_ELEVATION = 210
MAX_ELEVATION = 230

class Base():

    def __init__(self, numDams):
        self.numDams = numDams

    ######### Required Methods ############

    def getQopt(self, state, actionInd, dam):
        raise NotImplementedError()

    def incorporateObservations(self, state, actionInds, rewards, nextState, possibleActions):
        raise NotImplementedError()



    ########## Optional Methods ###########

    def outputStats(self, statsDir):
        pass

    def saveModel(self):
        pass

    def loadModel(self, state, possibleActions):
        pass


    ########## Common Helper Methods #########

    def discretizeState(self, state):
        (wbQIN, wbTIN, airTempForecast, solarFluxForecast, elevations, temps) = state

        wbQINindicators = np.empty([self.numDams,8])
        wbTINindicators = np.empty([self.numDams,6])
        for f in range(0, self.numDams):
            wbQINindicators[f,0] = int(wbQIN[f] <= 700)
            wbQINindicators[f,1] = int(wbQIN[f] > 700  and wbQIN[f] <= 1200)
            wbQINindicators[f,2] = int(wbQIN[f] > 1200  and wbQIN[f] <= 1700)
            wbQINindicators[f,3] = int(wbQIN[f] > 1700  and wbQIN[f] <= 2200)
            wbQINindicators[f,4] = int(wbQIN[f] > 2200  and wbQIN[f] <= 2700)
            wbQINindicators[f,5] = int(wbQIN[f] > 2700  and wbQIN[f] <= 3200)
            wbQINindicators[f,6] = int(wbQIN[f] > 3700  and wbQIN[f] <= 4200)
            wbQINindicators[f,7] = int(wbQIN[f] > 4200)
            wbTINindicators[f,0] = int(wbTIN[f] <= 12)
            wbTINindicators[f,1] = int(wbTIN[f] > 12 and wbTIN[f] <= 14)
            wbTINindicators[f,2] = int(wbTIN[f] > 14 and wbTIN[f] <= 16)
            wbTINindicators[f,3] = int(wbTIN[f] > 16 and wbTIN[f] <= 18)
            wbTINindicators[f,4] = int(wbTIN[f] > 18 and wbTIN[f] <= 20)
            wbTINindicators[f,5] = int(wbTIN[f] > 20)
        ##_print(wbQINindicators)
        ##_print(wbTINindicators)

        weatherJudgements = np.empty([self.numDams,2])
        airTempJudgement = int(airTempForecast > 65)
        solarFluxJudgement = int(solarFluxForecast > 300)
        weatherJudgements[f-1] = [airTempJudgement, solarFluxJudgement]

        elevationJudgements = np.zeros([self.numDams,23])
        elevationLevels = [210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230]
        for wb in range(self.numDams):
            lesser = np.array(elevationLevels) < elevations[wb]
            greater = np.array(elevationLevels) >= elevations[wb]-1
            if(np.sum(lesser) == 1):
                elevationJudgements[wb,0:21] = lesser.astype(int)
            elif(np.sum(greater) == 1):
                elevationJudgements[wb,0:21] = greater.astype(int)
            else:
                elevationJudgements[wb,0:21] = np.logical_and(lesser, greater).astype(int)
            if(np.sum(elevationJudgements) != 1):
                # we have lost, and are in the drained or overflow state
                if(elevations[wb] <= MIN_ELEVATION):
                    elevationJudgements[wb,-1] = 1
                elif(elevations[wb] >= MAX_ELEVATION):
                    elevationJudgements[wb,-2] = 1

                print elevations[wb]
                print lesser
                print greater
                print elevationJudgements
                print 'ERROR'
                raw_input("Press Enter to continue...")
            ##_print 'Elevation Judgements'
            ##_print elevation
            #_print elevationJudgements

        temperatureJudgements = (temps > 65).astype(int)

        # Construct State Array
        stateArray = elevationJudgements.flatten()
        stateArray = np.append(stateArray, weatherJudgements[0,0])
        stateArray = np.append(stateArray, temperatureJudgements.flatten())
        stateArray = np.append(stateArray, wbQINindicators)
        stateArray = np.append(stateArray, wbTINindicators)

        return stateArray
