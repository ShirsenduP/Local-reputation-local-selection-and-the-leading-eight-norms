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
	size = [250]
	density = [0.5] 
	distribution = [1.0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	socialNorm = 0
	omega = [0.99]

	# Model
	maxperiods = 3000
	socialDilemna = PrisonersDilemna(pdBenefit, pdCost)
	updateProbability = [0.1]
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
	print("Start")
	# logger.info("Simulation Initialising")
	N.runSimulation()
	# logger.info("Simulation Terminating")
	# results = N.results.export()
	print(N.results.strategyProportions[maxperiods-1])

	# plt.plot(results.strategyProportions[0])
	# plt.plot(results.strategyProportions[9])
	# plt.plot(results.utilities[0])
	# plt.plot(results.utilities[8])self.results.strategyProportions
	# plt.plot(results.actions['C'])
	# plt.plot(results.actions['D'])
	# plt.show()

	# print(N)

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



# TODO: UML diagram describing package - for dissertation
# TODO: Docstrings
# TODO: pandas dataframes BUG
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

"""

Dear Shirsendu,
I reviewed the structure of the original model of Othsuki and Isawa (2004), that we need to replicate as baseline model.

This is the structure i find, please note in particular the bold parts:

During time t, the following happens many times (until rand>omega \sim 1).
- one agent is selected, call it a
- another agent is selected, call it b
- consider focal agent a (same applies for b at the same time):
- a decides how to play based on its own behavioural strategy (each agent can have a different behavioural strategy)
- Thus agent  a with behavioural strategy p_{ab} take action Z (in the set {cooperate,defect}) depending on his own reputation and of the reputation of b.
- agents play their stategies and realize payoffs.

- reputation dynamics (shared at population level) attributes the reputation (aka H-score) d_{abX} (0 or 1) to a depending on reputation of a, reputation of b and action of a toward b.
- reputation dynamics (shared at population level) attributes the reputation (aka H-score) d_{baY} (0 or 1) to a depending on reputation of b, reputation of a and action of b toward a.

At the end of time t, evolutionary dynamics (replicator dynamics or social learning happens and a new population is created).


So basically: 
- reputation dynamics is 1 for each simulation (for all the population).
- behavioral strategy is different at individual level and evolves through the evolutionary dynamics.


this should clarify,

let me know and we talk tomorrow.

best,
Simone


Simone RIGHI
Lecturer | Financial Computing and Analytics Group
Department of Computer Science | University College London
Gower Street 66-72, London -- WC1E 6BT

Home Page: www.simonerighi.org


"""