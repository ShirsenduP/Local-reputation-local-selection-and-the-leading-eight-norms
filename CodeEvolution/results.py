import pandas as pd
import os
import json

class Results():

	def __init__(self):
		self.actions = {'C' : [], 'D' : []}
		self.strategyProportions = {}
		self.utilities = {}
		self.convergedAt = None

	def updateActions(self, actions):
		"""Given a dictionary of counts of cooperators and defectors, append to network results the proportions for that particular time period"""

		for key in actions:
			proportionAction = actions[key]/sum(actions.values())
			self.actions[key].append(proportionAction)


	# def export(self):
	# 	"""Return results of a single run of an experiment as a dataframe."""
	# 	actions = pd.DataFrame(self.actions)
	# 	strategyProportions = pd.DataFrame(self.strategyProportions)
	# 	utilities = pd.DataFrame(self.utilities)
	# 	results = pd.concat([actions, strategyProportions, utilities], axis=1)
	# 	return results

	def exportActions(self):
		actions = pd.DataFrame(self.actions)
		actions = actions.rename(columns={'C': 'Prop. of Cooperators', 'D': 'Prop. of Defectors'})
		return actions

	def exportCensus(self):
		#find strategies that are not present at the start of the simulation
		emptyKeys = []
		nonEmptyKeys = []
		for key, value in self.strategyProportions[0].items():
			if value == 0:
				emptyKeys.append(key)
			else:
				nonEmptyKeys.append(key)

		#remove strategies
		for key, value in self.strategyProportions.items():
			for emptyKey in emptyKeys:
				self.strategyProportions[key].pop(emptyKey, None)
		strats = pd.DataFrame(self.strategyProportions).transpose()
		strats = strats.add_prefix('Prop. Strategy #')
		return strats

	@classmethod
	def averageOverIterations(cls, iterations):
		"""Take a dictionary where each key is the iteration number and each value is the corresponding pandas dataframe of results. Return a single dataframe with averaged results."""
		# print(dict[0].column.values())
		iterationsAsList = list(iterations.values())
		concatenatedResults = pd.concat(iterationsAsList)
		byRowIndex = concatenatedResults.groupby(concatenatedResults.index)
		means = byRowIndex.mean()
		return means
		# return 0

	@classmethod
	def exportResultsToCSV(cls, experimentName, experimentConfig, experimentResults, experimentNumber):
		"""Export the results from a single dataframe averaged over multiple iterations as a 'experimentName.csv' file."""

		if experimentName not in os.listdir("CodeEvolution/results"):
			os.mkdir(f"CodeEvolution/results/{experimentName}")

		experimentResults.to_csv(f"CodeEvolution/results/{experimentName}/{experimentNumber}.csv")

		with open(f"CodeEvolution/results/{experimentName}/{experimentNumber}.txt", 'w') as f:
			f.write(json.dumps(experimentConfig.configuration)) # use `json.loads` to do the reverse


	def __str__(self):
		s = str(self.strategyProportions)
		s += 3*'\n'
		s += str(self.utilities)
		s += 3*'\n'
		s += str(self.actions)
		return s

