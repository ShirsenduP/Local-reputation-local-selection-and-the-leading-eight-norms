import random
from strategy import Strategy

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
		7: "lightpink"
	}

	def __init__(self, _id, _strategy):
		self.id = _id
		self.currentStrategy = Strategy(_strategy)
		self.currentReputation = random.choice(self.reputation)
		self.neighbours = []
		self.colour = self.strategyColour[self.currentStrategy.currentStrategyID]
		self.history = {} # get LAST partner

	def changeStrategy(self, newStrategyID):
		self.currentStrategy.changeStrategy(newStrategyID)

	def getOpponentsReputation(self, opponent):
		thirdParty = random.choice(opponent.neighbours)
		# randomly choose a neighbour of the opponent
		# return the result of their last interaction
	
	def summary(self):
		# s = "Summary of Network\n"
		s = f"Agent {self.id} is currently running strategy {self.currentStrategy} with current reputation {self.currentReputation}"
		return s

	def initialiseHistory(self):
		# neighbourIDs = [neighbour.id for neighbour in self.neighbours]
		# self.history = {}.fromkeys(neighbourIDs)
		self.history = {}.fromkeys(self.neighbours)

	def __str__(self):
		return str(self.id)

	# def __eq__(self, otherAgent):
	# 	return self.id == otherAgent.id

"""

TODO:

1. Rewrite self.neighbours to be a dictionary
	keys are neighbours
	values are dictionaries
		keys are chronological interaction
		values are the record of actions ijX and the resulting reputation for BOTH parties -> another dictionary?
2. __eq__ method to check if two agents are equal? It breaks the code currently, need to find oput why
"""


