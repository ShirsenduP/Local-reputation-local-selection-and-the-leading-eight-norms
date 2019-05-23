from argparse import ArgumentParser
import json
import time
import csv
import numpy as np
import pandas as pd

from network import Network
from socialdilemna import PrisonersDilemna
from results import averageOverIterations, exportResultsToCSV

if __name__=="__main__":
	description = "Run a single simulation from a JSON config file"
	filepathHelp = "Filepath to JSON config file"
	outputHelp = "Show final state of network"

	parser = ArgumentParser(description=description)
	parser.add_argument('filepath', metavar='F', help=filepathHelp, type=str)
	parser.add_argument('-o', '--output', help=outputHelp, action="store_true")
	args = parser.parse_args()

	
	with open(args.filepath) as config:	
		tests = json.load(config)


	experimentName = args.filepath.split(sep='/')[-1]
	numberOfExperiments = len(tests.keys())
	repeatPerExperiment = 100

	print(f"Total {numberOfExperiments} experiments")
	results = {}

	for experimentNumber in range(numberOfExperiments):
		dilemna = tests[str(experimentNumber)]['dilemna']
		for repeat in range(repeatPerExperiment):
			tests[str(experimentNumber)]['dilemna'] = PrisonersDilemna(dilemna[1], dilemna[2])
			N = Network(_config=tests[str(experimentNumber)])
			N.runSimulation()
			results[repeat] = N.results.export()
	
		# Average over all iterations
		experimentNumberResult = averageOverIterations(results)

		# Export a single CSV per experiment
		exportResultsToCSV(experimentName, experimentNumberResult, experimentNumber)
	
		print(".")

