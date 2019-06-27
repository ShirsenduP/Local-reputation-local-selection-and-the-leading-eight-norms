import random
import pandas as pd
import copy

from CodeEvolution.network import Network
from CodeEvolution.configbuilder import ConfigBuilder
from CodeEvolution.agent import Agent
from CodeEvolution.results import Results
from CodeEvolution.socialnorm import SocialNorm
from CodeEvolution.socialdilemna import SocialDilemna, PrisonersDilemna
from CodeEvolution.strategy import Strategy

class GrGe_Network(Network):
	"""Global Reputation, Global Evolution - AKA the model originating from Ohtsuki and Isawa's seminal Leading Eight paper on social norms. This model tries to verify the original results."""

	def __init__(self, _config):
		super().__init__(_config)
		if self.config['density'] != 1:
			self.config['density'] = 1
		self.createNetwork(agentType=GrGe_Agent)

	def getOpponentsReputation(self, agent1, agent2):
		"""(Global reputation - return the reputations of the two randomly chosen agents. The reputation of any agent is accessible to every other agent in the population."""
		return agent1.currentReputation, agent2.currentReputation

	def evolutionaryUpdate(self, alpha=10):
		"""Global Evolution - Find the strategy with the highest utility and the proportion of the utility over the utilities of all strategies."""

		strategyUtils = copy.deepcopy(self.results.utilities[self.currentPeriod])

		#find strategy with highest utility
		bestStrategy = max(strategyUtils, key=lambda key: strategyUtils[key])

		#check for strategies with negative utility
		for strategy, utility in strategyUtils.items():
			if utility < 0:
				strategyUtils[strategy] = 0

		#if total utility is zero, no evolutionary update
		totalUtil = sum(strategyUtils.values())
		if totalUtil == 0:
			return

		#probability of switching to strategy i is (utility of strategy i)/(total utility of all non-negative strategies)*(speed of evolution, larger the alpha, the slower the evolution)
		for strategy, _ in strategyUtils.items():
			strategyUtils[strategy] /= (totalUtil*alpha)
		
		for agent in self.agentList:
			r = random.random()
			if r < strategyUtils[bestStrategy]:
				agent.currentStrategy.changeStrategy(bestStrategy)

class GrGe_Agent(Agent):

	def __init__(self, _id, _strategy):
		super().__init__(_id, _strategy)
		self.history = None

	def updateStrategy(self, updateProbability):
		"""Overwrite the default update strategy method which implements local learning. Strategy updates occur in the network.evolutionaryUpdate method."""
		pass

def runExperiment(config, networkType=GrGe_Network, agentType=GrGe_Agent, repeat=10):
	results = {}
	for i in range(repeat):
		def simulate(config):
			N = networkType(config)
			N.runSimulation()
			resultsActions = N.results.exportActions()
			resultsCensus = N.results.exportCensus()
			resultsUtils = N.results.exportUtilities()
			return pd.concat([resultsActions, resultsCensus, resultsUtils], axis=1, sort=False)
		results[i] = simulate(config)
	meanResults = Results.averageOverIterations(results)
	return meanResults

if __name__ == "__main__":

	config = ConfigBuilder()
	R = runExperiment(config)
	print(R)
	# Results.exportResultsToCSV("test", config, R, 0)

	print("END")



	#TODO TESTS
	"""	1. starting 50/50 mutants and some Strategy
		2. Initially a strategy and no mutants - at the end of each timestep, each agent has some 'probabilityOfMutants' of turning into a mutant (<< .1 )
		3. test the number of mutants needed to kill the system"""