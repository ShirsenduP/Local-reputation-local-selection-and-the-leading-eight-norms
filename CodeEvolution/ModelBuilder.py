from json import dump
from argparse import ArgumentParser
from math import inf

from validator import Validator
from configbuilder import ConfigBuilder
from socialdilemna import PrisonersDilemna

if __name__=="__main__":

	parser = ArgumentParser(
		description="This script builds the configuration file to run a SINGLE simulation with the given parameters defined within the 'USER INPUT' section in the file 'ModelBuilder.py'.")
	args = parser.parse_args()

	#########################################################################################################
	### BEGIN USER INPUT
	#########################################################################################################

	# Experiment Name
	name = "draft"

	# Number of agents in network
	size = [50, 100, 150]

	# Density of connections in Erdos-Renyi randomly generated network (must be in [0,1])
	density = [0.6, 0.7, 0.8, 0.9] 
	
	# Probability distribution of agent strategies (must be floats and sum to 1)
	distribution = [0.5, 0.5, 0., 0., 0., 0., 0., 0.]
	
	# Probability of a further interaction within a single timeperiod (must be in (0,1))
	omega = [0.9]

	# Maximum number of periods run if no convergence (must be an integer greater than 1)
	maxperiods = 10

	# Social dilemna, payoff and cost ('PD' is the only acceptable social dilemna currently, benefit > cost)
	pdBenefit = 2
	pdCost = 1
	socialDilemna = ('PD', pdBenefit, pdCost)

	# Probability of any agent updating their strategy within a single time period (must be in [0,1])
	updateProbability = [0.2]

	# Mutant ID and Probability: [0,7] represent the leading eight, [8,9] represent All-D/All-C respectively
	mutantID = 8
	probabilityOfMutants = [0.01]

	#########################################################################################################
	### END USER INPUT
	#########################################################################################################
	
	# Parameter Input Validation
	Validator = Validator()
	Validator.checkPrisonerDilemnaParameters(pdBenefit, pdCost)
	Validator.checkNumeric([pdBenefit, pdCost])
	Validator.checkListTypes(size, int)
	Validator.checkRangeOfValuesInList(size, [0, inf], edges=False)
	Validator.checkListTypes(density, float)
	Validator.checkRangeOfValuesInList(density, [0, 1], edges=False)
	Validator.checkListTypes(distribution, float)
	Validator.checkRangeOfValuesInList(distribution, [0,1])
	Validator.checkValidDistribution(distribution)
	Validator.checkListTypes(omega, float)
	Validator.checkMaxPeriods(maxperiods)
	Validator.checkRangeOfValuesInList(updateProbability, [0, 1])
	Validator.checkRangeOfValuesInList(probabilityOfMutants, [0, 1], edges=False)


	# Generate config file
	singleSimulation = False
	saveToDisk = True

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

	# Export to configurations directory
	with open('CodeEvolution/configurations/{}.json'.format(name), 'w') as jsonConfig:
		dump(config.configuration, jsonConfig, indent=4)

	print(f"{len(config.configuration)} Experiments ready")

