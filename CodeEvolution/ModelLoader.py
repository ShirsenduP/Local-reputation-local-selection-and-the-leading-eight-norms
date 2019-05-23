import json
import profile

from argparse import ArgumentParser
from multiprocessing import Pool

from network import Network
from socialdilemna import PrisonersDilemna
from results import averageOverIterations, exportResultsToCSV

description = "Run a single simulation from a JSON config file"
filepathHelp = "Filepath to JSON config file"
outputHelp = "Show final state of network"
profilerHelp = "Run profiler and output to tests directory"

parser = ArgumentParser(description=description)
parser.add_argument('filepath', metavar='F', help=filepathHelp, type=str)
parser.add_argument('-o', '--output', help=outputHelp, action='store_true')
parser.add_argument('-p', '--profiler', help=profilerHelp, action='store_true')
args = parser.parse_args()

def main():
	
	with open(args.filepath) as config:	
		tests = json.load(config)


	experimentName = args.filepath.split(sep='/')[-1]
	numberOfExperiments = len(tests.keys())
	repeatPerExperiment = 3

	print(f"Total {numberOfExperiments} experiments")
	results = {}

	for experimentNumber in range(numberOfExperiments):
		print(f"Simulation {experimentNumber}/{numberOfExperiments}", end=" ", flush=True)
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

		print("\tdone")

	experimentInputs = list(range(numberOfExperiments))

if __name__=="__main__":
	main()

	
