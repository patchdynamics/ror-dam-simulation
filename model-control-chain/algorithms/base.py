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

    def loadModel(self, numStates, numActions):
        pass
