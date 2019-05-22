from argparse import ArgumentParser
import json
import time
import csv
import numpy as np

from network import Network
from socialdilemna import PrisonersDilemna

if __name__=="__main__":
	description = "Run a single simulation from a JSON config file"
	filepathHelp = "Filepath to JSON config file"
	outputHelp = "Show final state of network"

	parser = ArgumentParser(description=description)
	parser.add_argument('filepath', metavar='F', help=filepathHelp, type=str)
	parser.add_argument('-o', '--output', help=outputHelp, action="store_true")
	args = parser.parse_args()

	# with open(args.filepath) as config:
	# 	c = json.load(config)	

	# dilemna = c['dilemna']
	# print(len(c.keys()))

	# if dilemna[0] == 'PD':
	# 	PD = PrisonersDilemna(dilemna[1], dilemna[2])
	# 	c['dilemna'] = PD
	# else:
	# 	raise NotImplementedError(f"{dilemna[0]} has not been implemented yet, only 'PD' (str).")

	# N = Network(_config=c)
	
	# print("Simulation Start")

	# if args.output:
	# 	print(N)
		
	# N.runSimulation()
	
	# if args.output:
	# 	print(N)
	
	# print("\nSimulation Complete")

	experimentResults = []
	
	with open(args.filepath) as config:	
		tests = json.load(config)

	numberOfExperiments = len(tests.keys())
	repeatPerExperiment = 1

	print(f"Total {numberOfExperiments} experiments")

	for experimentNumber in range(numberOfExperiments):
		print('.', end=' ')
		dilemna = tests[str(experimentNumber)]['dilemna']
		tests[str(experimentNumber)]['dilemna'] = PrisonersDilemna(dilemna[1], dilemna[2])
		N = Network(_config=tests[str(experimentNumber)])
		N.runSimulation()
		experimentResults.append(N.results.export())


	np.savetxt("CodeEvolution/results/draft.csv", experimentResults, delimiter=',')
