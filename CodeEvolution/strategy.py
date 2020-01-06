import logging


class Strategy:
    
    allStates = ['11', '10', '01', '00']
    allOutcomes = [['C', 'D', 'C', 'C'],
                   ['C', 'D', 'C', 'C'],
                   ['C', 'D', 'C', 'D'],
                   ['C', 'D', 'C', 'D'],
                   ['C', 'D', 'C', 'D'],
                   ['C', 'D', 'C', 'D'],
                   ['C', 'D', 'C', 'D'],
                   ['C', 'D', 'C', 'D'],
                   ['D', 'D', 'D', 'D'],  # AllD
                   ['C', 'C', 'C', 'C']]  # AllC
    census = {}
    totalCountOfStrategies = 0

    def __init__(self, strategyID):
        Strategy.totalCountOfStrategies += 1
        self.currentStrategyID = strategyID
        self.currentStrategy = dict((key, value) for key, value in zip(Strategy.allStates, Strategy.allOutcomes[strategyID]))
        Strategy.updateCensus(strategyID, None)

    def chooseAction(self, agent1Reputation, agent2Reputation):
        stateKey = str(agent1Reputation) + str(agent2Reputation)
        return self.currentStrategy[stateKey]

    def changeStrategy(self, newStrategyID):
        Strategy.updateCensus(newStrategyID, self.currentStrategyID)
        self.currentStrategyID = newStrategyID
        self.currentStrategy = dict((key, value) for key, value in zip(self.allStates, self.allOutcomes[newStrategyID]))

    # @classmethod
    # def updateCensus(cls, newStrategyID, oldStrategyID=None):
    #     Strategy.census[newStrategyID] += 1
    #     if oldStrategyID != None:
    #         Strategy.census[oldStrategyID] -= 1
    #     if sum(Strategy.census.values()) != Strategy.totalCountOfStrategies:
    #         raise Exception("Number of strategies in census is greater than number of agents")

    @classmethod
    def updateCensus(cls, newID, oldID):
        if newID in Strategy.census.keys():
            # If strategy already exists in census then just increment counter
            Strategy.census[newID] += 1
        else:
            # If strategy does not exist, then create it
            Strategy.census[newID] = 1
        if oldID is not None:
            # If an agent switches from an old strategy, decrement the old strategy
            Strategy.census[oldID] -= 1

        # Error checking
        if sum(Strategy.census.values()) != Strategy.totalCountOfStrategies:
            logging.critical(f"Census({sum(Strategy.census.values())}) "
                             f"and total count of strategies ({Strategy.totalCountOfStrategies}) are out of "
                             f"balance!")

    @classmethod
    def reset(cls):
        Strategy.census = {}
        Strategy.totalCountOfStrategies = 0

    def __str__(self):
        return f"{self.currentStrategyID} - {self.currentStrategy}"


if __name__ == "__main__":
    pass

