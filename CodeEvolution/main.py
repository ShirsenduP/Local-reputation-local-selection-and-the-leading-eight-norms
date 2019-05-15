import random
import logging
from time import gmtime, strftime

from configbuilder import ConfigBuilder
from network import Network
from agent import Agent
from socialdilemna import PrisonersDilemna

def main():

	### Logging
	now = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
	logger = logging.getLogger('CodeEvolution')
	logger.setLevel(logging.INFO)
	# fh = logging.FileHandler(f'CodeEvolution/logs/{now}.log')
	fh = logging.FileHandler('CodeEvolution/logs/test.log')
	fh.setLevel(logging.DEBUG)
	ch = logging.StreamHandler()
	ch.setLevel(logging.ERROR)

	formatter = logging.Formatter('%(asctime)s \t%(levelname)s \t%(module)s \t%(funcName)s \t%(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)

	logger.addHandler(fh)
	logger.addHandler(ch)




	###
	### USER-INPUT
	###

	# Network
	size = [50]
	density = [0.6]
	omega = [0.9]
	

	# Model
	singleSimulation = True
	saveToDisk = False
	
	# Social PrisonersDilemna
	pdBenefit = 2
	pdCost = 1


	###
	### MODEL-GENERATED-PARAMETERS
	###

	config = ConfigBuilder(size, density, omega, singleSimulation, saveToDisk)
	PD = PrisonersDilemna(pdBenefit, pdCost)

	# Log message
	s = ""
	for key, value in config.configuration.items():
		s += f"{key}: \t {value}, "
	logger.info(f"Model parameters: \t {s}")
	
	###
	### MODEL
	###

	logger.info("Network Initialising")
	N = Network(config.configuration, PD)

	print(N)

	logger.info("Simulation Initialising")
	N.runSimulation()
	logger.info("Simulation Terminating")

	print(N)
	logger.info("Network Terminating")

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

7. agents are currently only initialised with 0/1 strategyIDs for debugging purposes
"""




