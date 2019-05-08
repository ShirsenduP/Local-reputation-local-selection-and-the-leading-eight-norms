import random
import colorsys

class Agent():

	strategies = (1,2,3,4,5,6,7,8)
	reputation = (-1,1)
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
		self.current_strategy = random.choice(self.strategies)
		self.current_reputation = random.choice(self.reputation)
		self.colour = self.strategyColour[self.current_strategy]

	def change_reputation(self):
		self.current_reputation *= -1
	
	def summary(self):
		# s = "Summary of Network\n"
		s = f"Agent {self.id} is currently running strategy {self.current_strategy} with current reputation {self.current_reputation}"
		return s

	def __str__(self):
		return str(self.id)
