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
from GrGe import GrGe_Agent, GrGe_Network

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
	probabilityOfMutants = [10]

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


	for i in range(5):
		N = GrGe_Network(config.configuration[0])
		N.createNetwork(GrGe_Agent)
		print("Start simulation {}".format(i))
		N.runSimulation()
		print(N.getCensusProportions())
		del N


if __name__ == "__main__":
	main()

# TODO: Priority
	# simones publications with karoly, 
	# otree behavioural experiments (look on simones page)
	# Nature, Science, Journal of theoretical biology, proceeding of the royal society, philosophical transcations of the royal society, AVOID behavioural economics

