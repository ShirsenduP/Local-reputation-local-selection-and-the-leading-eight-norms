import datetime
import json

from argparse import ArgumentParser
from configbuilder import ConfigBuilder
from socialdilemna import PrisonersDilemna


if __name__=="__main__":

	description = "Run a single simulation"
	sizeHelp = "Help: SIZE"
	densityHelp = "Help: DENSITY"
	omegaHelp = "Help: OMEGA"
	periodHelp = "Help: PERIODS"


	parser = ArgumentParser(description=description)
	parser.add_argument('--size', help=sizeHelp, type=int, nargs=1)
	parser.add_argument('--density', help=densityHelp, type=float, nargs=1)
	parser.add_argument('--omega', help=omegaHelp, type=float, nargs=1)
	parser.add_argument('--periods', help=periodHelp, type=int, nargs=1)
	args = parser.parse_args()

	# Social PrisonersDilemna
	pdBenefit = 2
	pdCost = 1

	# Network
	size = [50]
	density = [0.6] 
	omega = [0.99]

	# Model
	maxperiods = 1000
	socialDilemna = 'PD'
	updateProbability = [0.2]
	probabilityOfMutants = [0.01]
	singleSimulation = True
	saveToDisk = True

	config = ConfigBuilder(
		_sizes=size,
		_densities=density,
		_omegas=omega,
		_maxperiods=maxperiods,
		_socialDilemna=socialDilemna,
		_updateProbability=updateProbability,
		_probabilityOfMutants=probabilityOfMutants,
		_singleSimulation=singleSimulation,
		_saveToDisk=saveToDisk)



	timestamp = datetime.datetime.now()
	timestamp = timestamp.strftime("%d-%b-%Y_(%H:%M:%S.%f)")
	with open('CodeEvolution/configurations/jsonConfig@{}.json'.format(timestamp), 'w') as jsonConfig:
		json.dump(config.configuration, jsonConfig, indent=4)

	# config = ConfigBuilder(
	# 	_sizes=args.size,
	# 	_densities=args.density,
	# 	_omegas=args.omega,
	# 	_maxperiods=args.periods,
	# 	_socialDilemna=socialDilemna,
	# 	_updateProbability=updateProbability,
	# 	_probabilityOfMutants=probabilityOfMutants,
	# 	_singleSimulation=singleSimulation,
	# 	_saveToDisk=saveToDisk)

	# config.getJsonConfigFile()

"""

	TODO:

	1	'obj' should be the input into the network object or if there is an experiment object, lets see
	2	Need to add arguments for the social dilemna, default to PD, social norm etc 
	3	Add limits to parameters
	4 	Add help information/docstrings
	5	FIX SOCIAL DILEMNA LOADING INTO JSON/WORKAROUND


"""