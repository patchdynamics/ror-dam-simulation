from base import Base
import numpy as np
from sklearn.utils.extmath import cartesian
import random

KNN_FILE = "knn.npy"

NUM_NEIGHBORS = 5
NUM_POINTS_PER_DIM = 20
# TODO: Realistic min/max values
# State = (logQIN, TIN, airTemp, solarFlux, elevation, waterTemp)
#MIN_STATE = (6, 4, 0, 0, 210, 4)
#MAX_STATE = (9, 22, 45, 400, 230, 22)
MIN_STATE = (6, 215) # QIN = 403, elevation = 215
MAX_STATE = (8.85, 225) # QIN = 6974, elevation = 225

class KNN(Base):

    def __init__(self, numDams, stepsize, futureDiscount, possibleActions, numNeighbors):
        Base.__init__(self, numDams, stepsize, futureDiscount, possibleActions, numNeighbors)
        self.Qvalues = [{} for i in range(numDams)]
        (self.minList, self.maxList) = self.createListOfMinMaxStateValues()
        self.statePoints = self.createStatePoints()
        print self.statePoints.shape

    def createListOfMinMaxStateValues(self):
#        (minQIN, minTIN, minAirTempForecast, minSolarFluxForecast, minElevation, minTemp) = MIN_STATE
#        (maxQIN, maxTIN, maxAirTempForecast, maxSolarFluxForecast, maxElevation, maxTemp) = MAX_STATE
        (minQIN, minElevation) = MIN_STATE
        (maxQIN, maxElevation) = MAX_STATE

        # numDams dimensions for QIN, TIN, elevation. 3*numDams dimensions for temp
        # dimensions = 6 * self.numDams + 2
        minList = []
        maxList = []
        for i in range(self.numDams):
            minList.append(minQIN)
            maxList.append(maxQIN)
#        for i in range(self.numDams):
#            minList.append(minTIN)
#            maxList.append(maxTIN)
#        minList += [minAirTempForecast, minSolarFluxForecast]
#        maxList += [maxAirTempForecast, maxSolarFluxForecast]
        for i in range(self.numDams):
            minList.append(minElevation)
            maxList.append(maxElevation)
#        for i in range(3*self.numDams):
#            minList.append(minTemp)
#            maxList.append(maxTemp)
        return (np.array(minList), np.array(maxList))

    def createStatePoints(self):
        stateDimArrays = []
        for d in range(len(self.minList)):
            dimArray = np.linspace(self.minList[d], self.maxList[d], NUM_POINTS_PER_DIM)
            stateDimArrays.append(dimArray)
        return cartesian(stateDimArrays)

    def getStateArray(self, state):
        (wbQIN, wbTIN, airTempForecast, solarFluxForecast, elevations, temps) = state
        logQIN = np.log(wbQIN)
        #stateArray = np.array([airTempForecast, solarFluxForecast])
        #stateArray = np.concatenate((logQIN.flatten(), wbTIN.flatten(), stateArray, elevations.flatten(), temps.flatten()))
        stateArray = np.concatenate((logQIN.flatten(), elevations.flatten()))
        return stateArray

    # Normalize all state dimensions on [-1,1]
    def normalizeState(self, state):
        stateArray = self.getStateArray(state)
        return 2 * (stateArray - self.minList)/(self.maxList - self.minList) - 1

    def findNNs(self, state):
        stateArray = self.getStateArray(state)
        distances = np.linalg.norm(stateArray - self.statePoints, axis=1)
        NNs = np.argpartition(distances, NUM_NEIGHBORS)[:NUM_NEIGHBORS]
        probs = self.calculateProbs(distances[NNs])
        return (NNs, probs)

    # distances is array of distance to k nearest-neighbor states
    def calculateProbs(self, distances):
        weights = 1 / (1 + distances**2)
        return weights / np.sum(weights)

    def getQopt(self, state, actionInd, dam, neighbors, probs):
        NNQvalues = np.zeros(NUM_NEIGHBORS)
        for k in range(NUM_NEIGHBORS):
            neighborAction = (neighbors[k], actionInd)
            if neighborAction in self.Qvalues[dam]:
                NNQvalues[k] = self.Qvalues[dam][neighborAction]
        return np.sum(NNQvalues * probs)

    # Overwrite because too slow to do findNNs in getQopt and thus redo for every action!
    def getBestAction(self, state, dam):
        (neighbors, probs) = self.findNNs(state)

        (wbQIN, wbTIN, airTempForecast, solarFluxForecast, elevations, temps) = state
        actionQOUT = np.sum(self.possibleActions, 1)
        distances = (actionQOUT - wbQIN) ** 2
        allowedActions = np.argpartition(distances, 5)[:5]
        disallowedActions = [i for i in range(self.possibleActions.shape[0]) if i not in allowedActions]

        Qopts = np.empty(self.possibleActions.shape[0])
        for actionInd in range(self.possibleActions.shape[0]):
            Qopts[actionInd] = self.getQopt(state, actionInd, dam, neighbors, probs)
        Qopts[disallowedActions] = -float("inf")
        bestActionIndices = np.argwhere(Qopts == np.max(Qopts))
        bestActionInd = random.choice(bestActionIndices)[0]
        return bestActionInd, Qopts[bestActionInd]

    def incorporateObservations(self, state, actionInds, rewards, nextState):
        (neighbors, probs) = self.findNNs(state)
        for i in range(self.numDams):
            if not nextState: # Game over, no future rewards
                Vopt = 0
            else:
                [nextAction, Vopt] = self.getBestAction(nextState, i)
            print "Vopt", Vopt
            for k in range(NUM_NEIGHBORS):
                neighborAction = (neighbors[k], actionInds[i])
                oldQ = 0
                if neighborAction in self.Qvalues[i]:
                    oldQ = self.Qvalues[i][neighborAction]
                error = rewards[i] + self.futureDiscount * Vopt - oldQ
                self.Qvalues[i][neighborAction] = oldQ + self.stepsize * error * probs[k]


    def outputStats(self, statsDir):
        pass

    def saveModel(self):
        #for i in range(self.numDams):
        np.save(KNN_FILE, self.Qvalues)

    def loadModel(self, state):
        try:
            self.Qvalues = np.load(KNN_FILE)
            print "Restarting with existing Qvalues"
        except IOError:
            print "Starting with new Qvalues"
