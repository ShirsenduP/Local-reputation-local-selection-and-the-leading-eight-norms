import random
import logging
import numpy as np

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
		self.population = nx.Graph()
		self.erdosRenyiGenerator()
		self.snapshot = {}
		self.__initialiseAgentHistories()
		self.currentPeriod = 0
		self.results = Results()
		self.tempActions = {
			'C' : 0, 
			'D' : 0
		}

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



	def runSimulation(self):
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

	def erdosRenyiGenerator(self):
		strategyProbabilities = self.config['distribution']
		strategyDistribution = [np.random.choice(np.arange(0,len(strategyProbabilities)), p = strategyProbabilities) for _ in range(self.config['size'])]

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
						

	def playSocialDilemna(self):

		agent1, agent2 = self.chooseTwoAgents()

		agent2Reputation = agent1.getOpponentsReputation(agent2)
		agent1Reputation = agent2.getOpponentsReputation(agent1)
		
		logging.debug(f"agent {agent1.id} ({agent1.currentStrategy.currentStrategyID}) sees agent {agent2.id}'s reputation is {agent2Reputation}")
		logging.debug(f"agent {agent2.id} ({agent2.currentStrategy.currentStrategyID}) sees agent {agent1.id}'s reputation is {agent1Reputation}")

		agent1Move = agent1.currentStrategy.chooseAction(agent1.currentReputation, agent2Reputation)
		self.tempActions[agent1Move] += 1
		logging.debug(f"agent {agent1.id}'s move is {agent1Move}")

		agent2Move = agent2.currentStrategy.chooseAction(agent2.currentReputation, agent1Reputation)
		self.tempActions[agent2Move] += 1
		logging.debug(f"agent {agent2.id}'s move is {agent2Move}")
		
		# self.recordInteraction(agent1Move)
		# self.recordInteraction(agent2Move)
		payoff1, payoff2 = self.config['dilemna'].playGame(agent1Move, agent2Move)
		logging.debug(f"agent {agent1.id} gets payoff {payoff1}")
		logging.debug(f"agent {agent2.id} gets payoff {payoff2}")

		## Update agent utilities and reputations
		agent1.updateUtility(payoff1)
		agent2.updateUtility(payoff2)
		agent1.updateReputation(agent2Reputation, agent1Move)
		agent2.updateReputation(agent1Reputation, agent2Move)

		## Update interaction history
		agent1Interaction = {
			'Opponent': agent2,
			'Focal Reputation': agent1.currentReputation,
			'Opponent Reputation': agent2Reputation,
			'Focal Move': agent1Move, 
			'Opponent Move': agent2Move
		}
		# agent1.recordInteraction(agent1Interaction)		
		
		agent2Interaction = {
			'Opponent': agent1,
			'Focal Reputation': agent2.currentReputation,
			'Opponent Reputation': agent1Reputation,
			'Focal Move': agent2Move, 
			'Opponent Move': agent1Move
		}
		# agent2.recordInteraction(agent2Interaction)


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

	def grabSnapshot(self, period):
		self.snapshot[period] = self.agentList.copy()
		#TODO: Need to finish snapshot function for convergence check!

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
# TODO: record average utilities of each strategy
	


