import random
from strategy import Strategy
import logging

class Agent():

	reputation = (0,1)
	strategyColour = {
		0: "orange", 
		1: "tan",
		2: "palegreen",
		3: "turquoise",
		4: "cornflowerblue",
		5: "royalblue",
		6: "plum",
		7: "lightpink",
		8: "black",
		9: "green"
	}

	def __init__(self, _id, _strategy):
		self.id = _id
		self.currentStrategy = Strategy(_strategy)
		self.currentReputation = random.choice(self.reputation)
		self.currentUtility = 0
		self.neighbours = []
		self.history = {} # get LAST partner
		self.colour = self.strategyColour[self.currentStrategy.currentStrategyID]

	def updateUtility(self, payoff):
		"""Update the utility or cumulative payoff of an agent."""
		self.currentUtility += payoff

	def updateStrategy(self, updateProbability):
		"""Switch strategies to the strategy used by the best performing neighbour of the agent with some probability."""
		r = random.random()
		if r < updateProbability:
			newStrategyID = self.findBestLocalStrategy()
			if newStrategyID == self.currentStrategy:
				return
			if newStrategyID == 8:
				pass
				# print("update to mutant strat")
			self.currentStrategy.changeStrategy(newStrategyID)

	
		# TODO: Check how we find our own reputation, can't be hardcoded, has to be calculated using own social norm
		# TODO: Replicator dyamics (in model_experiment.pdf)
			
	
	def summary(self):
		# s = "Summary of Network\n"
		s = f"Agent {self.id} is currently running strategy {self.currentStrategy} with current reputation {self.currentReputation}"
		return s

	def initialiseHistory(self):
		"""Only keep track of interactions with your neighbours."""
		self.history = {}.fromkeys(self.neighbours)

	def recordInteraction(self, interaction):
		"""Remember the previous interaction with your neighbours (and no one else)."""
		if interaction['Opponent'] in self.neighbours:
			self.history[interaction['Opponent']] = interaction

	def getHistory(self):
		s = ""
		for neighbour in self.neighbours:
			s += f"Last interaction with neighbour {neighbour.id} was {self.history[neighbour]}\n"
		return s

	def findBestLocalStrategy(self):
		"""Find the strategy of your best performing neighbour. (Copy the best)"""
		neighbourUtilities = list(map(lambda x:x.currentUtility, self.neighbours))
		maxLocalUtility = max(neighbourUtilities)
		bestPerformingAgentIndex = neighbourUtilities.index(maxLocalUtility)
		return self.neighbours[bestPerformingAgentIndex].currentStrategy.currentStrategyID
	

	def __str__(self):
		s = f"Agent {self.id}\t"
		s += f"Strategy#: \t {self.currentStrategy.currentStrategyID}\t"
		s += f"Reputation: \t {self.currentReputation}\t"
		neighbourIDs = list(map(lambda neighbour:neighbour.id, self.neighbours))
		# s += f"Neighbours: \t {neighbourIDs}\t"
		s += f"Utility: \t {self.currentUtility}"
		return s



def main():
	pass

if __name__ == "__main__":
	main()



# TODO: findBestLocalStrategy -> What if multiple agents have the same utility but different strategies? random choice, right now its just updating to whichever one it finds first!
# TODO: findBestLocalStrategy -> social norm class with previous interaction history with some neighbour, if None, make random 1/0 choice
# TODO: reset payoff to 0 at the beginning of each timeperiod





