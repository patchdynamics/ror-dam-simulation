from base import Base
import numpy as np

QVALUES_FILE = "qvalues.npy"

class Lookup(Base):

    def __init__(self, numDams, stepsize, futureDiscount, possibleActions):
        Base.__init__(self, numDams, stepsize, futureDiscount, possibleActions)
        self.Qvalues = [{} for i in range(numDams)]

    def getQopt(self, state, actionInd, dam):
        stateAction = self.discretizeState(state).tolist()
        stateAction.append(actionInd)
        stateAction = tuple(stateAction)
        if stateAction in self.Qvalues[dam]:
            return self.Qvalues[dam][stateAction]
        return 0

    def incorporateObservations(self, state, actionInds, rewards, nextState):
        stateArray = self.discretizeState(state).tolist()
        for i in range(self.numDams):
            stateAction = stateArray.append(actionInds[i])
            [nextAction, Vopt] = self.getBestAction(nextState, i)
            oldQ = 0
            if stateAction in self.Qvalues[i]:
                oldQ = self.Qvalues[i][stateAction]

            error = rewards[i] + self.futureDiscount * Vopt - oldQ
            self.Qvalues[i][stateAction] = oldQ + self.stepsize * error

    def outputStats(self, statsDir):
        pass

    def saveModel(self):
        #for i in range(self.numDams):
        np.save(QVALUES_FILE, self.Qvalues)

    def loadModel(self, state):
        try:
            self.Qvalues = np.load(QVALUES_FILE)
            print "Restarting with existing Qvalues"
        except IOError:
            print "Starting with new Qvalues"
