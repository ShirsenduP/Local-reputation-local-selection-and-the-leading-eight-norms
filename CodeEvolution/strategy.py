class Strategy:
	
	allStates = ['11', '10', '01', '00']
	allOutcomes =  [['C', 'D', 'C', 'C'],
					['C', 'D', 'C', 'C'],
					['C', 'D', 'C', 'D'],
					['C', 'D', 'C', 'D'],
					['C', 'D', 'C', 'D'],
					['C', 'D', 'C', 'D'],
					['C', 'D', 'C', 'D'],
					['C', 'D', 'C', 'D']]


	def __init__(self, strategyID):
		self.currentStrategyID = strategyID
		self.currentStrategy = dict((key, value) for key, value in zip(self.allStates, self.allOutcomes[strategyID]))


	def chooseAction(self, agent1Reputation, agent2Reputation):
		stateKey = str(agent1Reputation) + str(agent2Reputation)
		return self.currentStrategy[stateKey]

	def changeStrategy(self, newStrategyID):
		self.currentStrategyID = newStrategyID
		self.currentStrategy = dict((key, value) for key, value in zip(self.allStates, self.allOutcomes[newStrategyID]))


"""

TODO:

1	Error checking to sanitise inputs
2	MAYBE change C/D to enumerate types? Not sure if necessary as user will never need to do this manually

"""