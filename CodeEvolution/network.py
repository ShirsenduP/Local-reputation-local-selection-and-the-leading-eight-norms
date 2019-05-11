import random

import matplotlib.pyplot as plt
import networkx as nx

from agent import Agent
from socialnorm import SocialNorm

class Network():

	def __init__(self, _size, _density, _omega, _socialNorm):
		self.size = _size
		self.density = _density
		self.omega = _omega
		self.agentList = []
		self.population = nx.Graph()
		self.erdosRenyiGenerator()
		self.currentTimeStep = 0
		self.socialNorm = SocialNorm(0)
		self.snapshot = {}

	def erdosRenyiGenerator(self):
		for agentID in range(self.size):
			self.agentList.append(Agent(_id=agentID, _strategy=random.randint(0,7)))
			self.population.add_node(self.agentList[agentID])

		for agentID1 in range(len(self.population)):
			for agentID2 in range(len(self.population)):
				if agentID1 != agentID2:
					r = random.random()
					if r < self.density:
						self.population.add_edge(self.agentList[agentID1], self.agentList[agentID2])
						if self.agentList[agentID2] not in self.agentList[agentID1].neighbours:
							self.agentList[agentID1].neighbours.append(self.agentList[agentID2])
						if self.agentList[agentID1] not in self.agentList[agentID2].neighbours:
							self.agentList[agentID2].neighbours.append(self.agentList[agentID1])
						
						
	def __getStrategyColours(self):
		colourMap = []
		for agent in self.agentList:
			colourMap.append(agent.colour)
		return colourMap


	def __playPrisonersDilemna(self, agent1, agent2):
		agent1.getOpponentReputation(agent2)
		agent2.getOpponentReputation(agent1)
		agent1.getMove()
		agent2.getMove()
		#play game
		#update reputations NOTE: from SocialNorm() class
		#update interaction history
		#social dilemnas -> use just b and c to get payoffs -> more general than the PD


	def chooseTwoAgents(self):
		agent1 = random.choice(self.agentList)
		agent2 = random.choice(self.agentList)
		print(agent2 == agent1)
		while agent2 == agent1:
			agent2 = random.choice(self.agentList)
		return [agent1.id, agent2.id]

	def runSingleTimestep(self):
		pass
	# 	interactionCounter = []
	# 	r = random.random()
	# 	while r < omega:


	def show(self):
		colourMap = self.__getStrategyColours()
		plt.subplot(111)
		nx.draw(self.population, with_labels=True, bold_text=True, node_color=colourMap)
		plt.show()
		# plt.savefig('/home/localadmin/Dev/CodeEvolution/CodeEvolution/figures/network.png')


	def summary(self):
		print("Network Summary")
		for agent in self.agentList:
			s = "Agent " + str(agent) + " has neighbours "
			for neighbour in agent.neighbours:
				s += str(neighbour.id)
			print(s)


    # def load_data(self):
    #     with open('tests/data/testfile0') as f:
    #         G = nx.read_adjlist(f, object=Agent)
    #     self.population = G


"""
TODO:
	
	- Add random seed to erdos renyi generator function -> predefined list of seeds for all repeated experiments
	- Implement load_from_file in constructor
	- plotting error
		MatplotlibDeprecationWarning: isinstance(..., numbers.Number); if cb.is_numlike(alpha):
"""