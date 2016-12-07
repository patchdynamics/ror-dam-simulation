from base import Base
import numpy as np


WEIGHTS_FILE = "weights.npy"

class Linear(Base):

    def __init__(self, numDams, stepsize, futureDiscount, possibleActions, numActionsPerState):
        Base.__init__(self, numDams, stepsize, futureDiscount, possibleActions, numActionsPerState)
        self.weights = None

    def getQopt(self, state, actionInd, dam):
        features = self.getFeatures(state, actionInd)
        return self.weights[dam].flatten().dot(features.flatten())


    def getFeatures(self, state, actionInd):
        stateArray = list(state)
        features = np.zeros((len(stateArray), self.possibleActions.shape[0]))
        features[:, actionInd] = stateArray # TODO: Add a bias term?
        return features


    def incorporateObservations(self, state, actionInds, rewards, nextState):
        #_print 'state'
        #_print state
        #_print 'next state'
        #_print nextState
        #_print 'rewards'
        #_print rewards
        #_print 'actionInds'
        #_print actionInds
        #_print 'weights'
        #_print weights
        stateArray = self.discretizeState(state).tolist()
        for i in range(self.numDams):
            features = self.getFeatures(stateArray, actionInds[i])
            if not nextState: # Game over, no future rewards
                Vopt = 0
            else:
                [nextAction, Vopt] = self.getBestAction(nextState, i)
            error = self.getQopt(stateArray, actionInds[i], i) - (rewards[i] + self.futureDiscount * Vopt)
            #_print 'Qopt   Vopt'
            #_print str(calculateQopt(state, actionInds[i], weights[i])) + '    ' + str(Vopt)
            self.weights[i] = self.weights[i] - self.stepsize * error * features
        #_print 'updated weights'
        #_print weights


    def outputStats(self, statsDir):
        for i in range(self.numDams):
            weightsFile = statsDir + "weights" + str(i+1) +".txt"
            with open(weightsFile, "a") as fout:
                np.savetxt(fout, self.weights[i].flatten(), newline=",")
                fout.write("\n")

    def saveModel(self):
        np.save(WEIGHTS_FILE, self.weights)
        print(self.weights)
        print(np.sum(self.weights))

    def loadModel(self, state):
        try:
            self.weights = np.load(WEIGHTS_FILE)
            print "Restarting with existing weights"
        except IOError:
            stateArray = self.discretizeState(state)
            self.weights = np.zeros((self.numDams, stateArray.shape[0], self.possibleActions.shape[0]))
            print "Starting with new weights"
