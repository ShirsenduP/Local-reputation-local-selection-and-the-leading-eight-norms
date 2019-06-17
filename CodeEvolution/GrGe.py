import random
import psutil

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
		if _config['density'] != 1:
			_config['density'] = 1
		self.createNetwork(agentType=GrGe_Agent)
		self.evolutionaryUpdateSpeed = 0.5

	def getOpponentsReputation(self, agent1, agent2):
		"""(Global reputation - return the reputations of the two randomly chosen agents. The reputation of any agent is accessible to every other agent in the population."""
		return agent1.currentReputation, agent2.currentReputation

	def updateInteractions(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
		"""With direct global access to reputations, interactions need not be recorded. Hence this method overides the default interaction saving mechanism for efficiency."""
		pass

	def updateReputation(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
		"""Assign reputations following an interaction with each agent's globally known reputation and not the calculated reputation as default."""

		agent1NewReputation = self.socialNorm.assignReputation(agent1.currentReputation, agent2.currentReputation, agent1Move)
		agent2NewReputation = self.socialNorm.assignReputation(agent2.currentReputation, agent1.currentReputation, agent2Move)

		agent1.updatePersonalReputation(agent1NewReputation)
		agent2.updatePersonalReputation(agent2NewReputation)

	def evolutionaryUpdate(self, alpha=10):
		"""Global Evolution - Find the strategy with the highest utility and the proportion of the utility over the utilities of all strategies."""

		strategyUtils = self.results.utilities[self.currentPeriod]

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
		
		# print(10*"_")
		# print(self.currentPeriod)
		for agent in self.agentList:
			r = random.random()
			if r < strategyUtils[bestStrategy]:
				agent.currentStrategy.changeStrategy(bestStrategy)

class GrGe_Agent(Agent):

	def __init__(self, _id, _strategy):
		super().__init__(_id, _strategy)
		self.history = None
		self.currentReputation = random.choice(self.reputation)

	def initialiseHistory(self):
		"""With global access to agent reputations, maintaining a history log is unnecessary."""
		pass

	def updateStrategy(self, updateProbability):
		"""Overwrite the default update strategy method which implements local learning. Strategy updates occur in the network.evolutionaryUpdate method."""
		pass






if __name__ == "__main__":




	###
	### MODEL-GENERATED-PARAMETERS
	###

	config = ConfigBuilder()
	#TODO: initialise the social dilemna object inside the network!!! pass parameters and type of SD into the config builder, and have the network create the social dilemna
	config = config.configuration[0]

	def runExperiment(config, networkType=Network, agentType=Agent, iter=10):
		experimentResults = {}
		for i in range(iter):
			print(".", end="")
			def simulate(config):
				N = networkType(config)
				N.runSimulation()
				print(N.getCensus())
				results = N.results.export()
				return results
			experimentResults[i] = simulate(config)
		return experimentResults

	R = runExperiment(config, networkType=GrGe_Network, agentType=GrGe_Agent, iter=5)
	means = Results.averageOverIterations(R)
	Results.exportResultsToCSV("test", means, 14)

	print("END")



	#TODO TESTS
	"""	1. starting 50/50 mutants and some Strategy
		2. Initially a strategy and no mutants - at the end of each timestep, each agent has some 'probabilityOfMutants' of turning into a mutant (<< .1 )
		3. test the number of mutants needed to kill the system"""