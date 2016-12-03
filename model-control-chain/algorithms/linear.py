from base import Base
import numpy as np


WEIGHTS_FILE = "weights.npy"

class Linear(Base):

    def __init__(self, numDams):
        Base.__init__(self, numDams)
        self.weights = None

    #TODO: state should be the raw real-valued state (& discretized in here...)


    def getFeatures(self, state, actionInd, shape):
        features = np.zeros(shape)
        features[:, actionInd] = state # TODO: Add a bias term?
        return features

    def getQopt(self, state, actionInd, dam):
        features = self.getFeatures(state, actionInd, self.weights[dam].shape)
        return self.weights.flatten().dot(features.flatten())

    def incorporateObservations(self, state, actionInds, rewards, nextState, possibleActions):
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
        for i in range(self.numDams):
            features = getFeatures(state, actionInds[i], self.weights[i].shape)
            #_print 'features'
            #_print features
            [nextAction, Vopt] = getBestAction(nextState, self.weights[i], possibleActions)
            error = calculateQopt(state, actionInds[i], i) - (rewards[i] + FUTURE_DISCOUNT * Vopt)
            #_print 'Qopt   Vopt'
            #_print str(calculateQopt(state, actionInds[i], weights[i])) + '    ' + str(Vopt)
            self.weights[i] = self.weights[i] - STEP_SIZE * error * features
        #_print 'updated weights'
        #_print weights
        return weights


    def outputStats(self, statsDir):
        for i in range(self.numDams):
            weightsFile = statsDir + "weights" + str(i+1) +".txt"
            with open(weightsFile, "a") as fout:
                np.savetxt(fout, self.weights[i].flatten(), newline=",")
                fout.write("\n")

    def saveModel(self):
        np.save(WEIGHTS_FILE, self.weights)
        print(weights)

    def loadModel(self, numStates, numActions):
        try:
            self.weights = np.load(WEIGHTS_FILE)
            print "Restarting with existing weights"
        except IOError:
            self.weights = np.zeros((self.numDams, numStates, numActions))
            print "Starting with new weights"
