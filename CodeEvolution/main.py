import random
import logging
import csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import gmtime, strftime

from configbuilder import ConfigBuilder
from network import Network
from agent import Agent
from socialdilemna import PrisonersDilemna

def main():

	### Logging
	now = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
	logger = logging.getLogger('CodeEvolution')
	logger.setLevel(logging.CRITICAL)
	# fh = logging.FileHandler(f'CodeEvolution/logs/{now}.log')
	fh = logging.FileHandler('CodeEvolution/logs/test.log')
	fh.setLevel(logging.CRITICAL)
	ch = logging.StreamHandler()
	ch.setLevel(logging.CRITICAL)

	formatter = logging.Formatter('%(asctime)s \t%(levelname)s \t%(module)s \t%(funcName)s \t%(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)

	logger.addHandler(fh)
	logger.addHandler(ch)

							
	###
	### USER-INPUT
	###
	
	# Social PrisonersDilemna
	pdBenefit = 2
	pdCost = 1

	# Network
	size = [50]
	density = [0.1] 
	distribution = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	omega = [0.9]

	# Model
	maxperiods = 500
	socialDilemna = PrisonersDilemna(pdBenefit, pdCost)
	updateProbability = [0.01]
	mutantID = 8
	probabilityOfMutants = [0.01]
	singleSimulation = True
	saveToDisk = False

	###
	### MODEL-GENERATED-PARAMETERS
	###

	config = ConfigBuilder(
		_sizes=size,
		_densities=density,
		_distribution=distribution,
		_omegas=omega,
		_maxperiods=maxperiods,
		_socialDilemna=socialDilemna,
		_updateProbability=updateProbability,
		_mutantID=mutantID,
		_probabilityOfMutants=probabilityOfMutants,
		_singleSimulation=singleSimulation,
		_saveToDisk=saveToDisk)




	# Log message
	s = ""
	for key, value in config.configuration.items():
		s += f"{key}: \t {value}, "
	logger.info(f"Model parameters: \t {s}")
	
	###
	### MODEL
	###

	logger.info("Network Initialising")
	N = Network(config.configuration)

	# print(N)
	print("Start")
	logger.info("Simulation Initialising")
	N.runSimulation()
	logger.info("Simulation Terminating")

	# print(N.results.actions)

	# plt.plot(N.results.strategyProportions[0])
	# plt.plot(N.results.strategyProportions[8])
	# plt.plot(N.results.utilities[0])
	# plt.plot(N.results.utilities[8])
	# plt.plot(N.results.actions['C'])
	# plt.plot(N.results.actions['D'])
	# plt.show()

	# np.savetxt("CodeEvolution/results/strategies.csv", N.results['strategies'], delimiter=',')
	# print(N)
	# print(N.results['strategies'])
	# print(N.results['averageUtility'])
	logger.info("Network Terminating")
	print("End")

	# p = pd.DataFrame(N.results['strategies'])
	# print(p)





if __name__ == "__main__":
	main()



# TODO: UML diagram describing package - for dissertation
# TODO: Docstrings
# TODO: pandas dataframes
# TODO: Output to csv -> class on it own
# TODO: Load the data into matplotlib
# TODO: Maybe add karoly on the github repo
# TODO: read karoly papers

# TODO: Priority
	# TODO: simones publications with karoly, 
	# TODO: write unit tests first 
	# TODO: logging functions
	# TODO: then reproduce iwasa paper
	# otree behavioural experiments (look on simones page)


# TODO: Nature, Science, Journal of theoretical biology, proceeding of the royal society, philosophical transcations of the royal society, AVOID behavioural economics