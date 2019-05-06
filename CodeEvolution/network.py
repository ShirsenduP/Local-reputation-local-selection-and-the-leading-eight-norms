import random

import matplotlib.pyplot as plt
import networkx as nx

from agent import Agent


class Network():

	def __init__(self, _size, _density):
		self.size = _size
		self.density = _density
		self.AgentList = []
		self.population = nx.Graph()
		self.__erdos_renyi_generator()

	def __erdos_renyi_generator(self):
		for agentID in range(self.size):
			self.AgentList.append(Agent(_id=agentID))
			self.population.add_node(self.AgentList[agentID])

		for agentID1 in range(len(self.population)):
			for agentID2 in range(len(self.population)):
				if agentID1 != agentID2:
					r = random.random()
					if r < self.density:
						self.population.add_edge(self.AgentList[agentID1], self.AgentList[agentID2])
						

	def show(self):
		plt.subplot(111)
		nx.draw(self.population, with_labels=True, bold_text=True)
		plt.show()

	def summary(self):
		print("Network Summary")
		for agent in self.AgentList:
			print(agent.summary())

    # def load_data(self):
    #     with open('tests/data/testfile0') as f:
    #         G = nx.read_adjlist(f, object=Agent)
    #     self.population = G

# NOTE:
# 	- Add random seed to erdos renyi generator function
#	- Implement load_from_file in constructor
