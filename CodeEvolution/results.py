class Results():

	def __init__(self):
		self.actions = {'C' : [], 'D' : []}
		self.strategyProportions = {}
		self.utilities = {}

	def updateActions(self, actions):
		"""Given a dictionary of counts of cooperators and defectors, append to network results the proportions for that particular time period"""

		for key in actions:
			proportionAction = actions[key]/sum(actions.values())
			self.actions[key].append(proportionAction)


	def export(self):
		"""Return results of a single run of an experiment as a tuple."""
		return (self.strategyProportions, self.utilities, self.actions)

	def __str__(self):
		s = str(self.strategyProportions)
		s += 3*'\n'
		s += str(self.utilities)
		s += 3*'\n'
		s += str(self.actions)
		return s