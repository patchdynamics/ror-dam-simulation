from base import Base
import numpy as np
from collections import defaultdict

QVALUES_FILE = "qvalues.npy"
CONVERGENCE_TOLERANCE = 0.01

class Lookup(Base):

    def __init__(self, numDams, stepsize, futureDiscount, possibleActions, numActionsPerState):
        Base.__init__(self, numDams, stepsize, futureDiscount, possibleActions, numActionsPerState)
        self.Qvalues = [{} for i in range(numDams)]
        self.transitions = [defaultdict(lambda: {}) for i in range(numDams)]
        self.stateRewards = [{} for i in range(numDams)]

    def getQopt(self, state, actionInd, dam):
        stateAction = list(state)
        stateAction.append(actionInd)
        stateAction = tuple(stateAction)
        if stateAction in self.Qvalues[dam]:
            return self.Qvalues[dam][stateAction]
        return 0

    def incorporateObservations(self, state, actionInds, rewards, nextState):
        stateArray = self.discretizeState(state).tolist()
        for i in range(self.numDams):
            stateAction = stateArray
            stateAction.append(actionInds[i])
            stateAction = tuple(stateAction)
            if not nextState: # Game over, no future rewards
                Vopt = 0
            else:
                [nextAction, Vopt] = self.getBestAction(nextState, i)
            oldQ = 0
            if stateAction in self.Qvalues[i]:
                oldQ = self.Qvalues[i][stateAction]

            error = rewards[i] + self.futureDiscount * Vopt - oldQ
            self.Qvalues[i][stateAction] = oldQ + self.stepsize * error

    def updateCounts(self, state, actionInds, rewards, nextState):
        stateArray = self.discretizeState(state).tolist()
        nextStateArray = tuple(self.discretizeState(nextState).tolist())
        for i in range(self.numDams):
            stateAction = stateArray
            stateAction.append(actionInds[i])
            stateAction = tuple(stateAction)
            if nextStateArray in self.transitions[i][stateAction]:
                self.transitions[i][stateAction][nextStateArray] += 1
            else:
                self.transitions[i][stateAction][nextStateArray] = 1
            self.stateRewards[i][nextStateArray] = rewards[i]

    def updateQvalues(self):
        for i in range(self.numDams):
            it = 0
            while (it == 0) or (maxDiff > CONVERGENCE_TOLERANCE):
                print "Value Iteration", it
                maxDiff = -float("inf")
                for stateAction in self.transitions[i]:
                    state = stateAction[:-1] # Last is the action
                    futureRewards = 0
                    for nextState in self.transitions[i][stateAction]:
                        [nextAction, Vopt] = self.getBestActionDiscretized(nextState, i)
                        transProb = self.transitions[i][stateAction][nextState] / len(self.transitions[i][stateAction])
                        futureRewards += transProb * Vopt

                    if stateAction in self.Qvalues[i]:
                        oldQ = self.Qvalues[i][stateAction]
                    else:
                        oldQ = float("inf")
                    self.Qvalues[i][stateAction] = self.stateRewards[i][state] + self.futureDiscount * futureRewards
                    if abs(oldQ - self.Qvalues[i][stateAction]) > maxDiff:
                        maxDiff = abs(oldQ - self.Qvalues[i][stateAction])
                it+=1

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
