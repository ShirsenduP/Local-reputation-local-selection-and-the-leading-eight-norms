class Strategy():
	
	allStates = ['11', '10', '01', '00']
	allOutcomes =  [['C', 'D', 'C', 'C'],
					['C', 'D', 'C', 'C'],
					['C', 'D', 'C', 'D'],
					['C', 'D', 'C', 'D'],
					['C', 'D', 'C', 'D'],
					['C', 'D', 'C', 'D'],
					['C', 'D', 'C', 'D'],
					['C', 'D', 'C', 'D'],
					['D', 'D', 'D', 'D'], #AllD
					['C', 'C', 'C', 'C']] #AllC
	census = {}.fromkeys(range(10), 0)
	totalCountOfStrategies = 0
	


	def __init__(self, strategyID):
		Strategy.totalCountOfStrategies += 1
		self.currentStrategyID = strategyID
		self.currentStrategy = dict((key, value) for key, value in zip(Strategy.allStates, Strategy.allOutcomes[strategyID]))
		self.updateCensus(strategyID, None)


	def chooseAction(self, agent1Reputation, agent2Reputation):
		stateKey = str(agent1Reputation) + str(agent2Reputation)
		return self.currentStrategy[stateKey]

	def changeStrategy(self, newStrategyID):
		self.updateCensus(newStrategyID, self.currentStrategyID)
		self.currentStrategyID = newStrategyID
		self.currentStrategy = dict((key, value) for key, value in zip(self.allStates, self.allOutcomes[newStrategyID]))

	def updateCensus(self, newStrategyID, oldStrategyID=None):
		Strategy.census[newStrategyID] += 1
		if oldStrategyID != None:
			Strategy.census[oldStrategyID] -= 1
		if sum(Strategy.census.values()) != Strategy.totalCountOfStrategies:
			raise Exception("Number of strategies in census is greater than number of agents")


	@classmethod
	def reset(cls):
		Strategy.census = {}.fromkeys(range(10),0)
		Strategy.totalCountOfStrategies = 0

	def __str__(self):
		return f"{self.currentStrategyID} - {self.currentStrategy}"

if __name__ == "__main__":
	pass

