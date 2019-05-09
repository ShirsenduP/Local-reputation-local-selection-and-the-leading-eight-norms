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
		pass
		# randomly choose a neighbour of the opponent
		# return the result of their last interaction
	
	def summary(self):
		# s = "Summary of Network\n"
		s = f"Agent {self.id} is currently running strategy {self.currentStrategy} with current reputation {self.currentReputation}"
		return s

	def __str__(self):
		return str(self.id)


