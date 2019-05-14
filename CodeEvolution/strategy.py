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

	def __str__(self):
		return f"{self.currentStrategyID} - {self.currentStrategy}"

def main():
	pass

if __name__ == "__main__":
	main()

"""

TODO:

1	Error checking to sanitise inputs -> no human interaction necessary, is this worth doing?

"""