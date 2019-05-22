import json

from argparse import ArgumentParser
from configbuilder import ConfigBuilder
from socialdilemna import PrisonersDilemna


if __name__=="__main__":

	description = "This script builds the configuration file to run a SINGLE simulation with the given parameters defined here"
	sizeHelp = "Help: The number (int (0,inf)) of agents in the network."
	densityHelp = "Help: The density (float (0,1]) of agent connections within the Erdos-Renyi generated random graph "
	omegaHelp = "Help: The probability (float (0,1)) of another interaction within the same timestep"
	periodHelp = "Help: The maximum number of iterations (int (0,inf)) allowed within the simulation"


	parser = ArgumentParser(description=description)
	parser.add_argument('--name', help="Name of JSON config file")
	# parser.add_argument('--size', help=sizeHelp, type=int, nargs=1)
	# parser.add_argument('--density', help=densityHelp, type=float, nargs=1)
	# parser.add_argument('--omega', help=omegaHelp, type=float, nargs=1)
	# parser.add_argument('--periods', help=periodHelp, type=int, nargs=1)
	args = parser.parse_args()

	# Social PrisonersDilemna
	pdBenefit = 2
	pdCost = 1

	# Network
	size = [50, 100, 150]
	density = [0.6, 0.7] 
	distribution = [0.5, 0.5, 0, 0, 0, 0, 0, 0]

	if sum(distribution) != 1:
		raise ValueError(f"Distribution {distribution} must sum to 1.")

	omega = [0.99]

	# Model
	maxperiods = 1000
	socialDilemna = ('PD', pdBenefit, pdCost)
	updateProbability = [0.2]
	mutantID = 8
	probabilityOfMutants = [0.01]
	singleSimulation = False
	saveToDisk = True

	if sum(distribution) != 1:
		raise ValueError
		
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


	with open('CodeEvolution/configurations/{}.json'.format(args.name), 'w') as jsonConfig:
		json.dump(config.configuration, jsonConfig, indent=4)

# TODO - Add limits to parameters