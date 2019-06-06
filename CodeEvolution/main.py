import random
import logging
import csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import gmtime, strftime

from CodeEvolution.configbuilder import ConfigBuilder
from CodeEvolution.network import Network
from CodeEvolution.agent import Agent
from CodeEvolution.socialdilemna import PrisonersDilemna
from CodeEvolution.strategy import Strategy

def main():
	# seed = 12
	# random.seed(seed)
	# np.random.seed(seed)

	### Logging
	# now = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
	# logger = logging.getLogger('CodeEvolution')

	# logger.setLevel(logging.DEBUG)
	# fh = logging.FileHandler('CodeEvolution/logs/test.log')
	# fh.setLevel(logging.DEBUG)
	# formatter = logging.Formatter('%(asctime)s \t%(levelname)s \t%(module)s \t%(funcName)s \t%(message)s')
	# fh.setFormatter(formatter)
	# logger.addHandler(fh)

							
	###
	### USER-INPUT
	###
	
	# Social PrisonersDilemna
	pdBenefit = 2
	pdCost = 1

	# Network
	size = [50]
	density = [0.1] 
	distribution = [0.9, 0, 0, 0, 0, 0, 0, 0, 0.1, 0]
	socialNorm = 0
	omega = [0.99]

	# Model
	maxperiods = 10
	socialDilemna = PrisonersDilemna(pdBenefit, pdCost)
	updateProbability = [0.99]
	mutantID = 8
	probabilityOfMutants = [0.1]

	###
	### MODEL-GENERATED-PARAMETERS
	###

	config = ConfigBuilder(
		_sizes=size,
		_densities=density,
		_distribution=distribution,
		_socialNorm=socialNorm,
		_omegas=omega,
		_maxperiods=maxperiods,
		_socialDilemna=socialDilemna,
		_updateProbability=updateProbability,
		_mutantID=mutantID,
		_probabilityOfMutants=probabilityOfMutants)




	# Log message
	# s = ""
	# for key, value in config.configuration.items():
	# 	s += f"{key}: \t {value}, "
	# logger.info(f"Model parameters: \t {s}")
	
	###
	### MODEL
	###

	# logger.info("Network Initialising")
	N = Network(config.configuration[0])
	N.createNetwork()
	# print(N)

	print("Start")
	# logger.info("Simulation Initialising")
	
	# print(N.getCensusProportions())

	N.runSimulation()
	# logger.info("Simulation Terminating")
	# results = N.results.export()
	# print(N.results.strategyProportions[maxperiods-1])

	# plt.plot(results.strategyProportions[0])
	# plt.plot(results.strategyProportions[9])
	# plt.plot(results.utilities[0])
	# plt.plot(results.utilities[8])self.results.strategyProportions
	# plt.plot(results.actions['C'])
	# plt.plot(results.actions['D'])
	# plt.show()

	# print(N)
	# print(N.results.strategyProportions[N.currentPeriod-1])
	# print(N.getCensusProportions())
	# np.savetxt("CodeEvolution/results/strategies.csv", N.results['strategies'], delimiter=',')
	# print(N.convergenceHistory)
	# print(N.results['strategies'])
	# print(N.results['averageUtility'])
	# logger.info("Network Terminating")
	print("End")

	# p = pd.DataFrame(N.results['strategies'])
	# print(p)





if __name__ == "__main__":
	main()

# TODO: Priority
	# simones publications with karoly, 
	# otree behavioural experiments (look on simones page)
	# Nature, Science, Journal of theoretical biology, proceeding of the royal society, philosophical transcations of the royal society, AVOID behavioural economics

