from argparse import ArgumentParser
import json

from network import Network
from socialdilemna import PrisonersDilemna

if __name__=="__main__":

	description = "Run a single simulation from a JSON config file"
	filepathHelp = "Filepath to JSON config file"


	parser = ArgumentParser(description=description)
	parser.add_argument('--file', help=filepathHelp, type=str)
	args = parser.parse_args()

	print(args.file)

	with open(args.file) as config:
		c = json.load(config)	

	benefit = 2
	cost = 1
	c['dilemna'] = PrisonersDilemna(benefit, cost)

	N = Network(_config=c)
	print("Simulation Start")
	N.runSimulation()
	print("Simulation Complete")

"""

	TODO:



"""

