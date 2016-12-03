import numpy as np

class Base():

    def __init__(self, numDams):
        self.numDams = numDams

    ######### Required Methods ############

    def getQopt(self, state, actionInd, dam):
        raise NotImplementedError()

    def incorporateObservations(self, state, actionInds, rewards, nextState, possibleActions):
        raise NotImplementedError()



    ########## Optional Methods ###########

    def outputStats(self, numDams):
        pass

    def saveModel(self):
        pass

    def loadModel(self, state, possibleActions):
        pass


    ########## Common Helper Methods #########

    def discretizeState(self, state):
        (QINs, TINs, airTempForecast, solarFluxForecast, elevations, temps) = state
        print QINs
        print TINs
        print airTempForecast
        print solarFluxForecast
        print elevations
        print temps

        wbQINindicators = np.empty([numDams,8])
        wbTINindicators = np.empty([numDams,6])
        for f in range(0, numDams):
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

        weatherJudgements = np.empty([numDams,2])
        airTempJudgement = int(airTempForecast > 65)
        solarFluxJudgement = int(solarFluxForecast > 300)
        weatherJudgements[f-1] = [airTempJudgement, solarFluxJudgement]

        elevationJudgements = np.zeros([numDams,23])
        elevationLevels = [210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230]
        lesser = np.array(elevationLevels) < elevation
        greater = np.array(elevationLevels) >= elevation-1
        if(np.sum(lesser) == 1):
            elevationJudgements[f-1,0:21] = lesser.astype(int)
        elif(np.sum(greater) == 1):
            elevationJudgements[f-1,0:21] = greater.astype(int)
        else:
            elevationJudgements[f-1,0:21] = np.logical_and(lesser, greater).astype(int)
        if(np.sum(elevationJudgements) != 1):
            # we have lost, and are in the drained or overflow state
            if(elevation <= MIN_ELEVATION):
                elevationJudgements[f-1,-1] = 1
            elif(elevation >= MAX_ELEVATION):
                elevationJudgements[f-1,-2] = 1
        ##_print 'Elevation Judgements'
        ##_print elevation
        #_print elevationJudgements
        if(np.sum(elevationJudgements) != 1):
            print elevation
            print lesser
            print greater
            print elevationJudgements
            print 'ERROR'
            raw_input("Press Enter to continue...")


        temperatureJudgements = np.zeros([numDams,3])
        temp220 = int(seg34ForTime[seg34ForTime[:,0].size - 15,1] > 65)
        temp202 = int(seg34ForTime[seg34ForTime[:,0].size - 11,1] > 65)
        temp191 = int(seg34ForTime[seg34ForTime[:,0].size - 6,1] > 65)

        # Construct State Array
        stateArray = elevationJudgements.flatten()
        stateArray = np.append(stateArray, weatherJudgements[0,0])
        stateArray = np.append(stateArray, temperatureJudgements.flatten())
        stateArray = np.append(stateArray, wbQINindicators)
        stateArray = np.append(stateArray, wbTINindicators)
