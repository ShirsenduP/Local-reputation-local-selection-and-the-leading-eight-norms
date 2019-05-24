import random
import logging
import numpy as np
from collections import OrderedDict

import matplotlib.pyplot as plt
import networkx as nx

from agent import Agent
from results import Results
from socialnorm import SocialNorm
from socialdilemna import SocialDilemna, PrisonersDilemna
from strategy import Strategy

logging.basicConfig(filename="CodeEvolution/logs/test.log", level=logging.DEBUG, format='%(asctime)s \t%(levelname)s \t%(module)s \t%(funcName)s \t%(message)s')

testSeed = 1
random.seed(testSeed)
np.random.seed(testSeed)

class Network():

	def __init__(self, _config):
		self.config = _config
		self.agentList = []
		self.socialNorm = SocialNorm(_config['socialNorm'])
		self.population = nx.Graph()
		self.erdosRenyiGenerator()
		self.__initialiseAgentHistories()
		self.currentPeriod = 0
		self.results = Results()
		self.tempActions = {
			'C' : 0, 
			'D' : 0
		}
		self.checkMinTwoNeighbours()
		self.convergenceHistory = OrderedDict()

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

		# count strategies and total utilities per strategy
		strategyIDs = self.results.strategyProportions.keys()
		strategies = {}.fromkeys(strategyIDs, 0)
		utilities = {}.fromkeys(strategyIDs, 0)
		for agent in self.agentList:
			agentStrategyID = agent.currentStrategy.currentStrategyID
			strategies[agentStrategyID] += 1		
			utilities[agentStrategyID] += agent.currentUtility


		for strategyID in utilities:
			if strategies[strategyID] > 0:
				utilities[strategyID] /= strategies[strategyID]

		# convert to proportions of the total population
		populationSize = self.config['size']
		for id in strategies:
			strategies[id] /= populationSize

		# update Results object with strategy proportions and average utilities
		for key, value in strategies.items():
			self.results.strategyProportions[key].append(value)
		for key, value in utilities.items():
			self.results.utilities[key].append(value)

	def compareNetworkState(self, state1, state2):
		pass
		# TODO: implement compareNetworkState(self, state1, state2)

	def runSimulation(self):
		
		convergenceCheckIntervals = random.sample(range(self.config['maxperiods']), 1)
		self.initStrategies()
		self.scanStrategies()
		mutantProbability = self.config['probabilityOfMutants']
		while self.currentPeriod < self.config['maxperiods']:
			self.resetUtility()
			self.resetTempActions()
			self.runSingleTimestep()
			self.scanStrategies()
			self.checkConvergence()
			r = random.random()
			if r < self.config['probabilityOfMutants']:
				self.addMutants(self.config['mutantID'], mutantProbability) 
			self.currentPeriod += 1
			self.results.updateActions(self.tempActions)
			if self.currentPeriod in convergenceCheckIntervals:
				self.grabSnapshot()

	def erdosRenyiGenerator(self):
		strategyProbabilities = self.config['distribution']
		strategyDistribution = [np.random.choice(np.arange(0,len(strategyProbabilities)), p = strategyProbabilities) for _ in range(self.config['size'])]

		for agentID in range(self.config['size']):
			randomStrategyIndex = random.randint(0, len(strategyDistribution)-1)
			self.agentList.append(Agent(_id=agentID, _strategy=strategyDistribution[randomStrategyIndex], _socialNorm=self.config['socialNorm']))
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
						


	def getOpponentsReputation(self, agent1, agent2):
		"""Calculate the reputation of your opponent given the last interaction of the opponent with a randomly chosen neighbour."""

		# NOTE: Only when two agents are interacting are their H-Score is calculated through the *population-wide* social norm, each agent could be imbued with their own H-score attribute but don't think its necessary -> might be if it takes too long to calculate each time. If any agent's previous interaction with their randomly chosen neighbour doesn't exist, then randomly choose a reputation

		agent2Neighbour = random.choice(agent2.neighbours)
		agent1Neighbour = random.choice(agent1.neighbours)
	
		agent2ThirdPartyInteraction = agent2.history[agent2Neighbour]
		agent1ThirdPartyInteraction = agent1.history[agent1Neighbour]

		try:
			agent2PastReputation = agent2ThirdPartyInteraction['Focal Reputation']
			agent2NeighbourPastReputation = agent2ThirdPartyInteraction['Opponent Reputation']
			agent2PastMove = agent2ThirdPartyInteraction['Focal Move']
		except:
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

		logging.debug(f"agent {agent1.id} ({agent1.currentStrategy.currentStrategyID}) sees agent {agent2.id}'s reputation is {agent2Reputation}")
		logging.debug(f"agent {agent2.id} ({agent2.currentStrategy.currentStrategyID}) sees agent {agent1.id}'s reputation is {agent1Reputation}")

		# Each agent calculates their move according to their behavioural strategy
		agent1Move = agent1.currentStrategy.chooseAction(agent1.currentReputation, agent2Reputation)
		self.tempActions[agent1Move] += 1
		logging.debug(f"agent {agent1.id}'s move is {agent1Move}")
		agent2Move = agent2.currentStrategy.chooseAction(agent2.currentReputation, agent1Reputation)
		self.tempActions[agent2Move] += 1
		logging.debug(f"agent {agent2.id}'s move is {agent2Move}")
		
		# Calculate each agent's payoff
		payoff1, payoff2 = self.config['dilemna'].playGame(agent1Move, agent2Move)
		logging.debug(f"agent {agent1.id} gets payoff {payoff1}")
		logging.debug(f"agent {agent2.id} gets payoff {payoff2}")

		# Update agent utilities and reputations
		agent1.updateUtility(payoff1)
		agent2.updateUtility(payoff2)
		# agent1.updateReputation(agent2Reputation, agent1Move)
		# agent2.updateReputation(agent1Reputation, agent2Move)

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


	def showHistory(self):
		for agent in self.agentList:
			s = f"History for agent {agent.id} \n"
			s += agent.getHistory()
			s += "\n"
			print(s)

	def checkConvergence(self):
		# TODO: Check convergence implementation
		pass


	def chooseTwoAgents(self):
		agent1 = random.choice(self.agentList)
		agent2 = random.choice(self.agentList)
		while agent2 == agent1:
			agent2 = random.choice(self.agentList)
		return [agent1, agent2]

	def addMutants(self, mutantStrategyID, proportion):
		newMutantCount = int(proportion*self.config['size'])
		addedMutants = []
		while len(addedMutants) < newMutantCount:
			randomMutant = random.choice(self.agentList)
			if randomMutant not in addedMutants:
				randomMutant.currentStrategy.changeStrategy(mutantStrategyID)
				addedMutants.append(randomMutant)

	def runSingleTimestep(self):
		self.playSocialDilemna()
		r = random.random()
		while r < self.config['omega']:
			self.playSocialDilemna()
			r = random.random()
		
		# Update strategies
		for agent in self.agentList:
			agent.updateStrategy(self.config['updateProbability'])

		# TODO: Grab snapshot

	def resetUtility(self):
		for agent in self.agentList:
			agent.currentUtility = 0

	def grabSnapshot(self):
		self.convergenceHistory[self.currentPeriod] = self.agentList.copy()

	def __initialiseAgentHistories(self):
		for agent in self.agentList:
			agent.initialiseHistory()


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

	
# TODO: Implement check for minimum 2 neighbours per agent
	


