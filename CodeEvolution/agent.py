import random

class Agent():

	
	strategies = (1,2,3,4,5,6,7,8)
	reputation = (0,1)
	strategyColour = {
		1: "tan",
		2: "palegreen",
		3: "turquoise",
		4: "cornflowerblue",
		5: "royalblue",
		6: "plum",
		7: "lightpink",
		8: "orange", 
	}

	def __init__(self, _id, _strategy=strategies[1]):
		self.id = _id
		self.currentStrategy = random.choice(self.strategies)
		self.currentReputation = random.choice(self.reputation)
		self.neighbours = []
		self.colour = self.strategyColour[self.currentStrategy]
		self.history = []

	def __playStrategy(self, strategy):
		pass

	def getOpponentsReputation(self, opponent):
		thirdParty = random.choice(opponent.neighbours)
		# randomly choose a neighbour of the opponent
		# return the result of their last interaction
	
	def summary(self):
		# s = "Summary of Network\n"
		s = f"Agent {self.id} is currently running strategy {self.currentStrategy} with current reputation {self.currentReputation}"
		return s

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