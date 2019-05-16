from argparse import ArgumentParser
from configbuilder import ConfigBuilder
import json

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

	config = ConfigBuilder(
		_sizes=args.size,
		_densities=args.density,
		_omegas=args.omega,
		_maxperiods=args.periods,
		_socialDilemna=socialDilemna,
		_updateProbability=updateProbability,
		_probabilityOfMutants=probabilityOfMutants,
		_singleSimulation=singleSimulation,
		_saveToDisk=saveToDisk)

	config.getJsonConfigFile()

"""

	TODO:

	1	'obj' should be the input into the network object or if there is an experiment object, lets see
	2	Need to add arguments for the social dilemna, default to PD, social norm etc 
	3	Add limits to parameters
	4 	Add help information/docstrings


"""