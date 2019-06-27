import random
import copy
import pandas as pd

from CodeEvolution.network import Network
from CodeEvolution.agent import Agent
from CodeEvolution.results import Results
from CodeEvolution.configbuilder import ConfigBuilder

class LrGe_Network(Network):
	"""Network with Local Reputation and Global Evolution (LrGe)"""
	
	def __init__(self, _config):
		super().__init__(_config)
		self.createNetwork(agentType=LrGe_Agent)

	def getOpponentsReputation(self, agent1, agent2):
		"""(Local reputation - return the reputations of the two randomly chosen agents. The reputation of any agent is accessible only to neighbours of that agent."""
		
		# Choose neighbour of each agent (except the opponent of that agent)
		agent2Neighbour = random.choice(agent2.neighbours)
		agent1Neighbour = random.choice(agent1.neighbours)
		while agent2Neighbour == agent1:
			agent2Neighbour = random.choice(agent2.neighbours)
		while agent1Neighbour == agent2:
			agent1Neighbour = random.choice(agent1.neighbours)

		# Get the agent's last interaction with their neighbour
		agent2ThirdPartyInteraction = agent2.history[agent2Neighbour]
		agent1ThirdPartyInteraction = agent1.history[agent1Neighbour]
		
		# Calculate agents' reputations using social norm, if no history, assign random reputation
		try:
			agent2PastReputation = agent2ThirdPartyInteraction['Focal Reputation']
			agent2NeighbourPastReputation = agent2ThirdPartyInteraction['Opponent Reputation']
			agent2PastMove = agent2ThirdPartyInteraction['Focal Move']
		except TypeError: #no previous interaction
			agent2Reputation = random.randint(0,1)
		else:
			agent2Reputation = self.socialNorm.assignReputation(agent2PastReputation, agent2NeighbourPastReputation, agent2PastMove)

		try:
			agent1PastReputation = agent1ThirdPartyInteraction['Focal Reputation']
			agent1NeighbourPastReputation = agent1ThirdPartyInteraction['Opponent Reputation']
			agent1PastMove = agent1ThirdPartyInteraction['Focal Move']
		except TypeError: #no previous interaction
			agent1Reputation = random.randint(0,1)
		else:
			agent1Reputation = self.socialNorm.assignReputation(agent1PastReputation, agent1NeighbourPastReputation, agent1PastMove)

		return (agent1Reputation, agent2Reputation)


	def evolutionaryUpdate(self, alpha=10):
		"""Global Evolution - Find the strategy with the highest utility and the proportion of the utility over the utilities of all strategies. COPIED FROM GrGe -> MAKE SURE ITS UP TO DATE UNTIL BETTER SOLUTION FOUND"""

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



class LrGe_Agent(Agent):

	def __init__(self, _id, _strategy):
		super().__init__(_id, _strategy)
		self.history = None

	def updateStrategy(self, updateProbability):
		"""Overwrite the default update strategy method which implements local learning. Strategy updates occur in the network.evolutionaryUpdate method."""
		pass

def runExperiment(config, networkType=LrGe_Network, agentType=LrGe_Agent, repeat=10):
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

