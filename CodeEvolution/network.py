import copy
import random
import logging
import numpy as np
from collections import deque

import matplotlib.pyplot as plt
import networkx as nx

from CodeEvolution.agent import Agent
from CodeEvolution.results import Results
from CodeEvolution.socialnorm import SocialNorm
from CodeEvolution.socialdilemna import SocialDilemna, PrisonersDilemna
from CodeEvolution.strategy import Strategy

# logging.basicConfig(filename="CodeEvolution/logs/test.log", level=logging.DEBUG, format='%(asctime)s \t%(levelname)s \t%(module)s \t%(funcName)s \t%(message)s')

# testSeed = 1
# random.seed(testSeed)
# np.random.seed(testSeed)

class Network():

	def __init__(self, _config):
		self.config = _config
		self.agentList = []
		self.socialNorm = SocialNorm(_config['socialNorm'])
		self.population = nx.Graph()
		# self.createNetwork()
		self.currentPeriod = 0
		self.results = Results()
		self.tempActions = {
			'C' : 0, 
			'D' : 0
		}
		self.checkMinTwoNeighbours()
		self.hasConverged = False
		self.convergenceCheckIntervals = random.sample(range(int(self.config['maxperiods']/4),self.config['maxperiods']), int(self.config['maxperiods']/50))
		self.convergenceCheckIntervals.sort()
		self.convergenceHistory = deque(3*[None], 3)

	def checkMinTwoNeighbours(self):
		"""Checks whether each node (agent) in the graph (network) has a minimum degree (#of neighbours) of 2."""

		for agent in self.agentList:
			# print(len(agent.neighbours))
			if len(agent.neighbours) < 2:
				raise Exception("One or more agents of this network does not satisfy the minimum two neighbours requirement. Try adjusting the density higher or increase the size of the network.")

	def resetTempActions(self):
		"""Reset the cooperation/defection counter to zero. To be used at the end of each timeperiod after actions have been recorded."""

		for action in self.tempActions:
			self.tempActions[action] = 0

	def initStrategies(self):
		"""Scan distribution of agent strategies to get the starting strategies."""
		
		dist = self.config['distribution']
		for id in range(len(dist)):
			if dist[id] != 0:
				self.results.strategyProportions[id] = []
				self.results.utilities[id] = []

		# Add mutant strategy as well
		mutantID = self.config['mutantID']
		self.results.strategyProportions[mutantID] = []
		self.results.utilities[mutantID] = []

	def scanStrategies(self):
		"""Update the results with the proportions of all strategies at any given time."""

		#update results with census		
		census = self.getCensusProportions()
		self.results.strategyProportions[self.currentPeriod] = census
		
		#add up all the utilities over the strategies
		censusCounts = self.getCensus()
		averageUtilities = {}.fromkeys(censusCounts.keys(), 0)
		for agent in self.agentList:
			agentStratID = agent.currentStrategy.currentStrategyID
			averageUtilities[agentStratID] += agent.currentUtility
			
		#average the utilities
		for ID, _ in averageUtilities.items():
			if censusCounts[ID] > 0:
				averageUtilities[ID] /= censusCounts[ID]

		#update results with utilities
		self.results.utilities[self.currentPeriod] = averageUtilities

	def runSimulation(self):
		self.initStrategies()
		self.scanStrategies()
		mutantProbability = self.config['probabilityOfMutants']
		while self.currentPeriod < self.config['maxperiods'] and not self.hasConverged:
			self.resetUtility()
			self.resetTempActions()
			self.runSingleTimestep()
			self.scanStrategies()
			r = random.random()
			if r < mutantProbability:
				self.addMutants(self.config['mutantID'], mutantProbability) 
			self.results.updateActions(self.tempActions)
			if self.currentPeriod in self.convergenceCheckIntervals:
				self.grabSnapshot()
				self.checkConvergence()

			if self.currentPeriod == 8:
				self.evolutionaryUpdate()

			if self.hasConverged or self.currentPeriod==self.config['maxperiods']-1:
				self.results.convergedAt = self.currentPeriod
				return
			else: 
				self.currentPeriod += 1

	def getStrategyCounts(self):
		"""Return a list where each element represents the strategyID of an agent"""

		populationSize = self.config['size']
		propOfStrategies = self.config['distribution']
		countsOfStrategies = [int(val*populationSize) for val in propOfStrategies]
		pop = []
		for i in range(len(countsOfStrategies)):
			for _ in range(countsOfStrategies[i]):
				pop.append(i)
		return pop
	
	def getCensus(self):
		"""Return a dictionary where the key-value pairs are the strategy IDs and the number of agents running that strategy."""
		censusCopy = copy.deepcopy(Strategy.census)
		return censusCopy

	def getCensusProportions(self):
		"""Return a dictionary where the key-value pairs are the strategy IDs and the proportion of the population running that strategy."""

		census = self.getCensus()
		size = self.config['size']
		for key, _ in census.items():
			census[key] /= size
		return census

	def createNetwork(self):
		"""Generate an Erdos-Renyi random graph with density as specified in the configuration class (configBuilder)."""

		strategyDistribution = self.getStrategyCounts()

		for agentID in range(self.config['size']):
			randomStrategyIndex = random.randint(0, len(strategyDistribution)-1)
			self.agentList.append(Agent(_id=agentID, _strategy=strategyDistribution[randomStrategyIndex]))
			strategyDistribution.pop(randomStrategyIndex)
			self.population.add_node(self.agentList[agentID])

		for agentID1 in range(len(self.population)):
			for agentID2 in range(len(self.population)):
				if agentID1 != agentID2:
					r = random.random()
					if r < self.config['density']:
						self.population.add_edge(self.agentList[agentID1], self.agentList[agentID2])
						if self.agentList[agentID2] not in self.agentList[agentID1].neighbours:
							self.agentList[agentID1].neighbours.append(self.agentList[agentID2])
						if self.agentList[agentID1] not in self.agentList[agentID2].neighbours:
							self.agentList[agentID2].neighbours.append(self.agentList[agentID1])

		self.__initialiseAgentHistories()

	def getOpponentsReputation(self, agent1, agent2):
		"""Calculate the reputation of your opponent given the last interaction of the opponent with a randomly chosen neighbour. Only when two agents are interacting are their H-Score is calculated through the *population-wide* social norm, each agent could be imbued with their own H-score attribute but don't think its necessary -> might be if it takes too long to calculate each time. If any agent's previous interaction with their randomly chosen neighbour doesn't exist, then randomly choose a reputation."""

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
		except:
			# No history so randomly assign a reputation
			agent2Reputation = random.randint(0,1)
		else:
			agent2Reputation = self.socialNorm.assignReputation(agent2PastReputation, agent2NeighbourPastReputation, agent2PastMove)

		try:
			agent1PastReputation = agent1ThirdPartyInteraction['Focal Reputation']
			agent1NeighbourPastReputation = agent1ThirdPartyInteraction['Opponent Reputation']
			agent1PastMove = agent1ThirdPartyInteraction['Focal Move']
		except:
			agent1Reputation = random.randint(0,1)
		else:
			agent1Reputation = self.socialNorm.assignReputation(agent1PastReputation, agent1NeighbourPastReputation, agent1PastMove)

		return (agent2Reputation, agent1Reputation)

	def playSocialDilemna(self):

		# Two agents chosen randomly from the population
		agent1, agent2 = self.chooseTwoAgents()
		agent2Reputation, agent1Reputation = self.getOpponentsReputation(agent1, agent2)

		# logging.debug(f"agent {agent1.id} ({agent1.currentStrategy.currentStrategyID}) sees agent {agent2.id}'s reputation is {agent2Reputation}")
		# logging.debug(f"agent {agent2.id} ({agent2.currentStrategy.currentStrategyID}) sees agent {agent1.id}'s reputation is {agent1Reputation}")

		# Each agent calculates their move according to their behavioural strategy
		agent1Move = agent1.currentStrategy.chooseAction(agent1.currentReputation, agent2Reputation)
		self.tempActions[agent1Move] += 1
		# logging.debug(f"agent {agent1.id}'s move is {agent1Move}")
		agent2Move = agent2.currentStrategy.chooseAction(agent2.currentReputation, agent1Reputation)
		self.tempActions[agent2Move] += 1
		# logging.debug(f"agent {agent2.id}'s move is {agent2Move}")
		
		# Calculate each agent's payoff
		payoff1, payoff2 = self.config['dilemna'].playGame(agent1Move, agent2Move)
		# logging.debug(f"agent {agent1.id} gets payoff {payoff1}")
		# logging.debug(f"agent {agent2.id} gets payoff {payoff2}")

		# Update agent utilities and reputations
		agent1.updateUtility(payoff1)
		agent2.updateUtility(payoff2)
		self.updateReputation(agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move)


		# Update interaction history
		agent1Interaction = {
			'Opponent': agent2,
			'Focal Reputation': agent1.currentReputation,
			'Opponent Reputation': agent2Reputation,
			'Focal Move': agent1Move, 
			'Opponent Move': agent2Move
		}
		agent1.recordInteraction(agent1Interaction)		
		
		agent2Interaction = {
			'Opponent': agent1,
			'Focal Reputation': agent2.currentReputation,
			'Opponent Reputation': agent1Reputation,
			'Focal Move': agent2Move, 
			'Opponent Move': agent1Move
		}
		agent2.recordInteraction(agent2Interaction)

	def updateReputation(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
		"""Given the agents, their reputations, and their moves, update their personal reputations (the reputation they use for themselves for all of their interactions)."""
		agent1PersonalReputation = self.socialNorm.assignReputation(agent1.currentReputation, agent2Reputation, agent1Move)
		agent2PersonalReputation = self.socialNorm.assignReputation(agent2.currentReputation, agent1Reputation, agent2Move)

		agent1.updatePersonalReputation(agent1PersonalReputation)
		agent2.updatePersonalReputation(agent2PersonalReputation)

	def showHistory(self):
		for agent in self.agentList:
			s = f"History for agent {agent.id} \n"
			s += agent.getHistory()
			s += "\n"
			print(s)

	def checkConvergence(self):
		"""Check if the network has converged or not by checking the last 3 snapshots taken at randomly chosen intervals."""
		
		history = self.convergenceHistory

		# Minimum 3 snapshots needed to check for convergence (as defined in self.convergenceHistory)
		if None in history:
			return

		if history[2] == history[1] and history[1] == history[0]:
			self.hasConverged = True
			self.results.convergedAt = self.currentPeriod

	def chooseTwoAgents(self):
		agent1 = random.choice(self.agentList)
		agent2 = random.choice(self.agentList)
		while agent2 == agent1:
			agent2 = random.choice(self.agentList)
		return (agent1, agent2)

	def addMutants(self, mutantStrategyID, proportion):
		newMutantCount = int(proportion*self.config['size'])
		addedMutants = []
		while len(addedMutants) < newMutantCount:
			randomMutant = random.choice(self.agentList)
			if randomMutant not in addedMutants:
				randomMutant.currentStrategy.changeStrategy(mutantStrategyID)
				addedMutants.append(randomMutant)

	# def evolutionaryUpdate(self):
	# 	"""Calculate the distribution of utilities over the various strategies and reallocate the strategies of members in the same proportions. E.g. if Strategy 1 and 2 at the end of a timestep have average utility 5 and 10, then the strategy distribution for the next round for Strategies 1 and 2 should be 33%/66%."""
	# 	populationSize = self.config['size']
	# 	currentCensus = list(self.getCensusProportions().values())
		
	# 	currentUtils = self.results.utilities[self.currentPeriod]
	# 	print("Strategy Distribution: ", self.getCensusProportions())
	# 	print("Utility Distribution: ", currentUtils)
	# 	# If the average utility of a strategy is negative, why would anyone switch to it? Remove it from the distribution
	# 	for key, _ in currentUtils.items():
	# 		if currentUtils[key]<0:
	# 			currentUtils[key] = 0
	# 	print("Utility Distribution: ", currentUtils)

	# 	totalAvgUtil = sum(currentUtils.values())
	# 	if totalAvgUtil == 0:
	# 		return
		
	# 	# Get distribution of utilities per strategy
	# 	finalCensus = [round(util/totalAvgUtil, 3) for util in currentUtils.values()]


	# 	difference = [round(y-x,2) for x, y in zip(currentCensus, finalCensus)]
	# 	if sum([abs(x) for x in difference]) == 0:
	# 		print("system converged to 1 strategy")
	# 		return

	# 	strategySwaps = [(i, thing) for i, thing in zip(list(range(10)), difference) if round(thing,3) != 0]
	# 	print(strategySwaps)


	# 	print("Strategy Update: ", strategySwaps)
	# 	assert len(strategySwaps) <= 2
	# 	if strategySwaps[0][1] > 0:
	# 		strategySwaps.reverse()
		
	# 	for agent in self.agentList:
	# 		if agent.currentStrategy.currentStrategyID == strategySwaps[0][0]:
	# 			r = random.random()
	# 			if r < strategySwaps[1][1]*self.config['updateProbability']:
	# 				print(f"Agent {agent.id}, sOld={agent.currentStrategy.currentStrategyID}, r={r}, sNew={strategySwaps[1][0]}")
	# 				agent.currentStrategy.changeStrategy(strategySwaps[1][0])
	# 			else:
	# 				print("no update")
	# 		else:
	# 			print(f"Agent {agent.id}, sOld={agent.currentStrategy.currentStrategyID}, nochange!")

	# 	print("New Strategy Distribution: ", self.getCensusProportions())

	def evolutionaryUpdate(self, alpha):
		"""Calculate the distribution of utilities over the various strategies and reallocate the strategies of members in the same proportions. E.g. if Strategy 1 and 2 at the end of a timestep have average utility 5 and 10, then the strategy distribution for the next round for Strategies 1 and 2 should be 33%/66%."""

		startingDistribution = self.getCensusProportions()

		# If the population is already dominated by a single strategy then strategy update is not possible (this could emerge by only a single strategy in the population)
		activeStrategies = {}
		for key, value in startingDistribution.items():
			if value > 0:
				activeStrategies[key] = value
		
		if len(activeStrategies) == 1:
			print("skipped")
			return
		elif len(activeStrategies) > 2:
			raise Exception("more than 2 strategies in the population -> should not happen currently!")

		# We only care about strategies with positive utilities
		strategyUtils = self.results.utilities[self.currentPeriod]
		activeUtils = {}.fromkeys(activeStrategies)
		for key, value in strategyUtils.items():
			if key in activeStrategies.keys():
				activeUtils[key] = strategyUtils[key] if strategyUtils[key] > 0 else 0
		totalUtil = sum(activeUtils.values())


		# Find target distribution weighted by alpha
		target = {}.fromkeys(activeStrategies)
		for key, value in target.items():
			util = activeUtils[key]
			target[key] = (1-alpha)*activeStrategies[key] + alpha*(util/totalUtil)

		# Find proportion of population changing strategies
		change = {}.fromkeys(target)
		for key, value in target.items():
			change[key] = round(target[key] - activeStrategies[key],4)

		order = [None, None]
		for key, value in change.items():
			if value < 0:
				order[0] = key
			else:
				order[1] = key
		losingStrategy, growingStrategy = order

		for agent in self.agentList:
			if agent.currentStrategy.currentStrategyID == losingStrategy:
				r = random.random()
				if r < abs(target[growingStrategy]):
					agent.currentStrategy.changeStrategy(growingStrategy)
			
		print()
		print("strats: ", activeStrategies)
		print("utils: ", activeUtils)
		print("target: ", target)
		print("change: ", change)
		print("losing strat: ", losingStrategy)
		print("growing strat: ", growingStrategy)
		print("new strats: ", self.getCensusProportions())







	#TODO: 
	# smooth evolutionary strategy update
	# final distribution of strategies defined same as proportions of payoffs, so you have a goal distribution of updated strategies, then you cycle throughe each agent and each agent updates with some probability defined by us

	#TODO:
	# Faster the speed of evolution (omega), the lower the proportion of cooperators

	#TODO:
	# Global reputation but local update, you copy from your neighbours, but interact with everybody
		

	def runSingleTimestep(self):
		self.playSocialDilemna()
		r = random.random()
		while r < self.config['omega']:
			self.playSocialDilemna()
			r = random.random()
		
		# Update strategies
		for agent in self.agentList:
			agent.updateStrategy(self.config['updateProbability'])
			# print(f"Agent {agent.id} updating to {agent.currentStrategy.currentStrategyID}")

		# if self.currentPeriod in self.convergenceHistory


	def resetUtility(self):
		for agent in self.agentList:
			agent.currentUtility = 0

	def grabSnapshot(self):
		self.convergenceHistory.appendleft(self.getCensus())

	def __initialiseAgentHistories(self):
		for agent in self.agentList:
			agent.initialiseHistory()
		#TODO: change so histories and list of neighbours is the same thing!!

	def __getStrategyColours(self):
		colourMap = []
		for agent in self.agentList:
			colourMap.append(agent.colour)
		return colourMap

	def show(self):
		colourMap = self.__getStrategyColours()
		plt.subplot(111)
		nx.draw(self.population, with_labels=True, bold_text=True, node_color=colourMap)
		plt.show()
		# plt.savefig('/home/localadmin/Dev/CodeEvolution/CodeEvolution/figures/network.png')

	def __str__(self):
		s = ""
		for agent in self.agentList:
			s += str(agent) + "\n"
		return s


def main():
	pass

if __name__ == "__main__":
	main()

	
# TODO: when distribution*size doesn't give integer values, fix so it converts to int and adjusts the agent strategy counts	


