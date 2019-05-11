import matplotlib.pyplot as plt
import networkx as nx
import random

from network import Network
from agent import Agent
from socialnorm import SocialNorm
from configbuilder import ConfigBuilder

def main():

	sizes = [10000]
	densities = [0.5]
	omegas = [0.5]
	#proportions of agents = {
	# s1:
	# s2:
	# s3:}

	# config = ConfigBuilder(sizes, densities, omegas)


	socialNorm = SocialNorm(0)
	size = 20
	density = 0.5
	omega = 0.1
	# saveToDisk = False

	# config = ConfigBuilder(size, density, omega, saveToDisk)
	# print(config)

	# N = Network(config)
	N = Network(_size=size, _density=density, _omega=omega, _socialNorm=socialNorm)
	N.show()
	# N.summary()
	# N.runSimulation()
	
	# G = nx.erdos_renyi_graph(20, 1)
	# plt.subplot(111)
	# nx.draw(G)
	# plt.show()
	# print(len(G))
	print("success")
	return 0

if __name__ == "__main__":
	main()



"""

TODO:

1. Setup as package so it can easily be installed on any linux system with help docs. 
2. Create builder class to setup parameters of model, then change Network class to just accept a builder object to seperate the config methods to the simulation methods
3. When adding neighbours, don't add if already neighbours! repeated agents in agent.neighbours list!
4. DOCSTRINGS!!!
5. SocialDilemna class -> subclasses can be input to network to choose and parameterise the game easily


"""




