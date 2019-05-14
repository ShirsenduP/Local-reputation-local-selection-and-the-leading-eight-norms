import random

from configbuilder import ConfigBuilder
from network import Network
from agent import Agent
from socialdilemna import PrisonersDilemna

def main():

	###
	### USER-INPUT-PARAMETERS
	###

	size = [5]
	density = [1]
	omega = [0.5]
	singleSimulation = True
	saveToDisk = False
	pdBenefit = 2
	pdCost = 1

	###
	### MODEL-GENERATED-PARAMETERS
	###

	config = ConfigBuilder(size, density, omega, singleSimulation, saveToDisk)
	PD = PrisonersDilemna(pdBenefit, pdCost)

	###
	### MODEL
	###

	N = Network(config.configuration, PD)
	# agents = N.runSingleTimestep()

	print(N)

	for period in range(10000):
		N.playSocialDilemna()

	# N.showHistory()


	print(N)
	

	print("success")


if __name__ == "__main__":
	main()



"""

TODO:
1. Setup as package so it can easily be installed on any linux system with help docs. 
2. Create builder class to setup parameters of model, then change Network class to just accept a builder object to seperate the config methods to the simulation methods
3. When adding neighbours, don't add if already neighbours! repeated agents in agent.neighbours list!
5. SocialDilemna class -> subclasses can be input to network to choose and parameterise the game easily

4. DOCSTRINGS!!!
6. UML diagram to explain class structure

"""




