import random

class Agent():

	strategies = (1,2,3,4,5,6,7,8)
	reputation = (-1,1)

	def __init__(self, _id, _strategy=strategies[1]):
		self.id = _id
		self.current_strategy = random.choice(self.strategies)
		self.current_reputation = random.choice(self.reputation)
		# self.colour = strategy_colours[self.current_strategy]
		self.colour = 0

	def change_reputation(self):
		self.current_reputation *= -1
	
	def summary(self):
		# s = "Summary of Network\n"
		s = f"Agent {self.id} is currently running strategy {self.current_strategy} with current reputation {self.current_reputation}"
		return s

	def __str__(self):
		return str(self.id)

# TODO:
# 	- fix summary, add summary of network method in network class