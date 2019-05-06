import random
from CodeEvolution.__constants import get_global_constants

strategies = get_global_constants()


class Agent():

	def __init__(self, _id, _strategy=strategies[1]):
		self.id = _id
		self.current_strategy = random.choice(strategies)
		self.current_reputation = 1
		# self.colour = strategy_colours[self.current_strategy]
		self.colour = 0

	def change_reputation(self):
		self.current_reputation *= -1
	
	def __str__(self):
		s = f"Agent {self.id} is currently running strategy {self.current_strategy} with current reputation {self.current_reputation} \n"
		return s