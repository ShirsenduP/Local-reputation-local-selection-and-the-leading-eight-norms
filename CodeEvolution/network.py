import random
import logging

import matplotlib.pyplot as plt
import networkx as nx

from agent import Agent
from socialnorm import SocialNorm
from socialdilemna import SocialDilemna, PrisonersDilemna
from strategy import Strategy

logging.basicConfig(filename="CodeEvolution/logs/test.log", level=logging.DEBUG, format='%(asctime)s \t%(levelname)s \t%(module)s \t%(funcName)s \t%(message)s')

class Network():

	def __init__(self, _config, _socialDilemna):
		self.config = _config
		self.agentList = []
		self.population = nx.Graph()
		self.erdosRenyiGenerator()
		self.socialDilemna = _socialDilemna
		self.snapshot = {}
		self.__initialiseAgentHistories()
		self.maxPeriods = 10
		self.updateProbability = 0.2
		self.finished = False

	def erdosRenyiGenerator(self):
		for agentID in range(self.config['size']):
			self.agentList.append(Agent(_id=agentID, _strategy=random.randint(0,7)))
			# self.agentList.append(Agent(_id=agentID, _strategy=random.randint(2,3)))
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
		logging.debug(f"agent {agent1.id}'s move is {agent1Move}")

		agent2Move = agent2.currentStrategy.chooseAction(agent2.currentReputation, agent1Reputation)
		logging.debug(f"agent {agent2.id}'s move is {agent2Move}")
		
		payoff1, payoff2 = self.socialDilemna.playGame(agent1Move, agent2Move)
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
		agent1.recordInteraction(agent1Interaction)		
		
		agent2Interaction = {
			'Opponent': agent1,
			'Focal Reputation': agent2.currentReputation,
			'Opponent Reputation': agent1Reputation,
			'Focal Move': agent2Move, 
			'Opponent Move': agent1Move
		}
		agent2.recordInteraction(agent2Interaction)

		# agent1.showHistory()
		# agent2.showHistory()

	def showHistory(self):
		for agent in self.agentList:
			s = f"History for agent {agent.id} \n"
			s += agent.getHistory()
			s += "\n"
			print(s)
			
	def runSimulation(self):
		currentPeriod = 0
		probOfMutants = 0.01
		while currentPeriod < self.maxPeriods:
			self.runSingleTimestep()
			currentPeriod += 1
			#self.checkConvergence()
			r = random.random()
			if r < probOfMutants:
				# print("Mutants added")
				self.addMutants(8, 0.2)
			# print(self)	
		self.finished = True

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
		# Interaction Period
		self.playSocialDilemna()
		r = random.random()
		interactionCounter = 1
		while r < self.config['omega']:
			self.playSocialDilemna()
			interactionCounter += 1
			r = random.random()
		
		# Update strategies
		for agent in self.agentList:
			agent.updateStrategy(self.updateProbability)

		# NEED TO MAKE SNAPSHOT

	def grabSnapshot(self, period):
		self.snapshot[period] = self.agentList.copy()
		

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
		# print("Network Summary")
		# for agent in self.agentList:
		# 	s = "Agent " + str(agent) + f" with reputation {agent.currentReputation} has neighbours \t" 
		# 	for neighbour in agent.neighbours:
		# 		s += "\t" + str(neighbour.id)
		# 	print(s)
		if self.finished:
			s = "FINAL STATE\n"
		else:
			s = "INITIAL STATE\n"

		for agent in self.agentList:
			s += str(agent) + "\n"
		return s




    # def load_data(self):
    #     with open('tests/data/testfile0') as f:
    #         G = nx.read_adjlist(f, object=Agent)
    #     self.population = G


def main():
	pass

if __name__ == "__main__":
	main()

"""
TODO:
	
	- Implement check for minimum 2 neighbours per agent
	- Add random seed to erdos renyi generator function -> predefined list of seeds for all repeated experiments
	- Implement load_from_file in constructor
	- plotting error
		MatplotlibDeprecationWarning: isinstance(..., numbers.Number); if cb.is_numlike(alpha):
	- record current timesteps/interactions per period?
	- record proportions of different strategies at each timestep
	- record average utilities of each strategy
	
"""

