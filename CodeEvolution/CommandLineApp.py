from argparse import ArgumentParser
from configbuilder import ConfigBuilder

if __name__=="__main__":

	description = "Run a single simulation"
	sizeHelp = "Help: SIZE"
	sizeDensity = "Help: DENSITY"
	sizeOmega = "Help: OMEGA"


	parser = ArgumentParser(description=description)
	parser.add_argument('--size', help=sizeHelp, type=int, nargs=1)
	parser.add_argument('--density', help=sizeDensity, type=float, nargs=1)
	parser.add_argument('--omega', help=sizeOmega, type=float, nargs=1)
	args = parser.parse_args()

	obj = ConfigBuilder(_sizes=args.size, _densities=args.density, _omegas=args.omega)

	print(obj.configuration)

	print("NOT IMPLEMENTED")




	
"""

	TODO:

	1	'obj' should be the input into the network object or if there is an experiment object, lets see
	2	Need to add arguments for the social dilemna, default to PD, social norm etc 
	3	Add limits to parameters
	4 	Add help information/docstrings


"""