import pandas as pd
import os

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


	def export(self):
		"""Return results of a single run of an experiment as a dataframe."""
		actions = pd.DataFrame(self.actions)
		strategyProportions = pd.DataFrame(self.strategyProportions)
		utilities = pd.DataFrame(self.utilities)
		results = pd.concat([actions, strategyProportions, utilities], axis=1)
		return results


	@classmethod
	def averageOverIterations(cls, iterations):
		"""Take a dictionary where each key is the iteration number and each value is the corresponding pandas dataframe of results. Return a single dataframe with averaged results."""
		# print(dict[0].column.values())
		result = pd.DataFrame()
		iterationsAsList = list(iterations.values())
		concatenatedResults = pd.concat(iterationsAsList)
		byRowIndex = concatenatedResults.groupby(concatenatedResults.index)
		means = byRowIndex.mean()
		return means

	@classmethod
	def exportResultsToCSV(cls, experimentName, experimentResults, experimentNumber):
		"""Export the results from a single dataframe averaged over multiple iterations as a 'experimentName.csv' file."""

		if experimentName not in os.listdir("CodeEvolution/results"):
			os.mkdir(f"CodeEvolution/results/{experimentName}")

		experimentResults.to_csv(f"CodeEvolution/results/{experimentName}/{experimentName}-{experimentNumber}.csv")

	def __str__(self):
		s = str(self.strategyProportions)
		s += 3*'\n'
		s += str(self.utilities)
		s += 3*'\n'
		s += str(self.actions)
		return s

