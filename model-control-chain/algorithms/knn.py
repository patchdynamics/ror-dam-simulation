from base import Base
import numpy as np
from sklearn.utils.extmath import cartesian

KNN_FILE = "knn.npy"

NUM_NEIGHBORS = 5
NUM_POINTS_PER_DIM = 2
#TODO: Realistic min/max values
MIN_STATE = ((500, 4, 0, 0, 210, 4))
MAX_STATE = ((7000, 22, 45, 400, 230, 22))

class KNN(Base):

    def __init__(self, numDams, stepsize, futureDiscount, possibleActions):
        Base.__init__(self, numDams, stepsize, futureDiscount, possibleActions)
        (self.minList, self.maxList) = self.createListOfMinMaxStateValues()
        self.statePoints = self.createStatePoints()
        print self.statePoints.shape
        self.initQvalues()

    def createListOfMinMaxStateValues(self):
        (minQIN, minTIN, minAirTempForecast, minSolarFluxForecast, minElevation, minTemp) = MIN_STATE
        (maxQIN, maxTIN, maxAirTempForecast, maxSolarFluxForecast, maxElevation, maxTemp) = MAX_STATE
        # numDams dimensions for QIN, TIN, elevation. 3*numDams dimensions for temp
        # dimensions = 6 * self.numDams + 2
        minList = []
        maxList = []
        for i in range(self.numDams):
            minList.append(minQIN)
            maxList.append(maxQIN)
        for i in range(self.numDams):
            minList.append(minTIN)
            maxList.append(maxTIN)
        minList += [minAirTempForecast, minSolarFluxForecast]
        maxList += [maxAirTempForecast, maxSolarFluxForecast]
        for i in range(self.numDams):
            minList.append(minElevation)
            maxList.append(maxElevation)
        for i in range(3*self.numDams):
            minList.append(minTemp)
            maxList.append(maxTemp)
        print minList
        return (np.array(minList), np.array(maxList))

    def createStatePoints(self):
        stateDimArrays = []
        for d in range(len(self.minList)):
            dimArray = np.linspace(self.minList[d], self.maxList[d], NUM_POINTS_PER_DIM)
            stateDimArrays.append(dimArray)
        return cartesian(stateDimArrays)

    def initQvalues(self):
        pointActions = cartesian(self.statePoints, self.possibleActions)
        damQvalues = {pa: 0 for pa in pointActions }
        self.Qvalues = [damQvalues for i in range(self.numDams)]
        print len(damQvalues)

    def getStateArray(self, state):
        (wbQIN, wbTIN, airTempForecast, solarFluxForecast, elevations, temps) = state
        stateArray = np.array([airTempForecast, solarFluxForecast])
        stateArray = np.concatenate((wbQIN.flatten(), wbTIN.flatten(), stateArray, elevations.flatten(), temps.flatten()))
        return stateArray

    # Normalize all state dimensions on [-1,1]
    def normalizeState(self, state):
        stateArray = self.getStateArray(state)
        return 2 * (stateArray - self.minList)/(self.maxList - self.minList) - 1

    def findNNs(self, state):
        stateArray = self.getStateArray(state)
        distances = np.linalg.norm(stateArray - self.statePoints, axis=1)
        print distances.shape
        NNs = np.argpartition(distances, NUM_NEIGHBORS)[:NUM_NEIGHBORS]
        print NNs
        return (NNs, distances[NNs])

    # distances is array of distance to k nearest-neighbor states
    def calculateProbs(self, distances):
        weights = 1 / (1 + distances**2)
        return weights / np.sum(weights)

    def getQopt(self, state, actionInd, dam):
        (neighbors, distances) = self.findNNs(state)
        probs = self.calculateProbs(distances)
        NNQvalues = np.empty(NUM_NEIGHBORS)
        for k in range(NUM_NEIGHBORS):
            neighborAction = (neighbors[k], actionInd)
            print type(neighborAction)
            NNQvalues[k] = self.Qvalues[dam][neighborAction]
        return np.sum(NNQvalues * probs)

    def incorporateObservations(self, state, actionInds, rewards, nextState):
        raise NotImplementedError()

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
