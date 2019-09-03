import logging
import os
import time
import copy

import numpy as np
import pandas as pd
from tqdm import trange

from CodeEvolution.strategy import Strategy
from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork, LrLeERNetwork, LrGeRRLNetwork
from CodeEvolution.config import Config
from CodeEvolution.config import Population, State
from CodeEvolution.results import Results
from CodeEvolution.structures import RandomRegularLattice


class Experiment:
    """This class generates a series of Config objects to run for a single experiment. Define a 'default' experiment,
     then choose (a SINGLE) variable to be varied, then add the list of values the variable will cycle through."""

    def __init__(self, networkType, variable=None, values=None, defaultConfig=Config(), repeats=100):
        self.networkType = networkType
        self.default = defaultConfig
        self.variable = variable
        self.values = values
        self.experiments = None
        self.repeats = repeats
        if defaultConfig.degree is not None:
            defaultConfig.density = None

        self.generateConfigs()

    def generateConfigs(self):
        """Given a variable and the range of values to be tested for that variable, generate a list of Config objects
        for each of those tests"""
        if self.variable is None or self.values is None:
            raise ValueError("Parameters 'variable' and 'values' must not be None.")

        if self.variable == 'population':
            # Changing the initial state/population is an edge-case because of the multiple changes needed to be made
            tests = []
            for i in range(len(self.values)):
                newConfig = copy.deepcopy(self.default)
                tests.append(newConfig)
                setattr(tests[i], 'population',
                        Population(ID=self.values[i][0].ID, proportion=self.values[i][0].proportion))
                setattr(tests[i], 'mutant',
                        Population(ID=self.values[i][1].ID, proportion=self.values[i][1].proportion))
                setattr(tests[i], 'socialNormID', self.values[i][0].ID)
        else:
            # General Case
            tests = []
            for i in range(len(self.values)):
                newConfig = copy.deepcopy(self.default)
                tests.append(newConfig)
                setattr(tests[i], self.variable, self.values[i])

        # If degree is something that is being tests, assign the new density
        if self.default.degree is not None or self.variable is 'degree':
            self.assignNewDensitiesFromDegree(tests)

        self.experiments = tuple(tests)
        # print(self.experiments)

    def showExperiments(self, asString=False):
        """Print to the console a condensed list of all the config files in the object's experiment list."""
        s = str()
        for thing in self.experiments:
            s += str(thing.__dict__) + 2 * "\n"

        if asString:
            return s
        else:
            print(s)

    def run(self, export=False, display=False, recordFull=False, displayFull=False, cluster=False):
        """Run and export LocalData for an experiment. This by default exports only the final state of the simulation,
        so the proportions of cooperators/defectors, the final proportions of each strategy. With the optional flag
        'recordFull', every time-step is recorded and then averaged. THIS IS NOT YET FULLY FUNCTIONAL as issues occur
         when multiple of the same parameterised run have different lengths of simulations. Cluster takes precedence
         over export."""

        experimentName = self.networkType.name + "_" + self.variable + "_" + time.strftime("%Y-%m-%d %H:%M:%S")

        # Only prepare LocalData area if working locally, if running on Pycharm console, it will throw an error but its
        # purely aesthetic so just ignore it
        try:
            if not cluster:
                Results.initialiseOutputDirectory(experimentName)
                _, columnWidth = os.popen('stty size', 'r').read().split()
                nameLength = len(experimentName)
                columnWidth = int(columnWidth)
                print("\nRunning  ", experimentName, (columnWidth - nameLength - 11) * "=")
        except ValueError:
            pass

        if recordFull:
            raise NotImplementedError("Recording the full data releases data often incorrectly. Do not use.")

        # run all tests in the experiment
        for exp in trange(len(self.experiments), leave=True):
            if display:
                print(f"\nExperiment {exp} with {self.variable} at {self.values[exp]}")

            # Run a single test with [1,inf) repeats
            singleTest = pd.DataFrame()
            for _ in trange(self.repeats, leave=False):
                Strategy.reset()
                singleRun = self.simulate(self.experiments[exp], self.networkType, displayFull)
                singleTest = pd.concat([singleTest, singleRun], sort=False)
                Strategy.reset()

            if display:
                print()
                print(singleTest)
                print()

            # Export to different places if running locally/on a cluster
            if cluster:
                Results.exportResultsToCsvCluster(experimentName, self.experiments[exp], singleTest, exp)
            elif export:
                Results.exportResultsToCsv(experimentName, self.experiments[exp], singleTest, exp)

        # Export config text file
        configs = self.showExperiments(asString=True)
        Results.exportExperimentConfigs(configs, experimentName)

        try:
            if not cluster:
                print("\nFinished ", experimentName, (columnWidth - nameLength - 11) * "=")
        except Exception:
            pass

    @staticmethod
    def assignNewDensitiesFromDegree(testsList):
        """Given a list of config objects, overwrite densities of networks given the degree for a d-regular graph."""
        for exp in testsList:
            actualDensity = RandomRegularLattice.getTheoreticalDensity(exp)
            s = f"Density of {exp.density} overwritten by "
            exp.density = actualDensity
            s += f"{actualDensity}"
            logging.debug(s)

    @staticmethod
    def generateParameterFile(defaultConfig, variable, values, repeats):
        """(BETA) Export a parameters file (.txt) for UCL clusters"""

        if None in [variable, values]:
            raise ValueError("Parameters 'variable' and 'values' must not be None.")

        with open('params.txt', 'w') as f:
            counter = 0
            for exp in range(len(values)):
                for rep in range(repeats):
                    args = f"{counter:04d} "  # Simulation ID
                    args += str(variable) + " "
                    args += str(values[exp]) + "\n"
                    f.write(args)
                    counter += 1

        logging.info(f"Parameter file generated in {os.getcwd()}.")

    @staticmethod
    def simulate(m_exp, networkType, displayFull):
        """Perform a single run of any given test and export LocalData as a dataframe with one row with the final
        LocalData of the run."""

        # Run simulation
        N = networkType(m_exp)
        N.runSimulation()

        # Export LocalData in pandas DataFrames
        resultsActions = N.results.exportActions()
        resultsCensus = N.results.exportCensus()
        resultsUtils = N.results.exportUtilities()
        resultsMutations = N.results.exportMutations().sum()
        # print(resultsMutations)

        # Combine LocalData
        resultsFull = pd.concat([resultsCensus, resultsActions, resultsUtils], axis=1, sort=False)

        if displayFull:
            print(resultsFull)

        # Housekeeping: rename index
        resultsFull.index.names = ['Tmax']

        # Get only final time-step information and total number of mutants added
        resultsAtTmax = resultsFull.tail(1).copy()
        resultsAtTmax['# of Mutants Added'] = resultsMutations
        return resultsAtTmax

    @staticmethod
    def generatePopulationList(strategies=tuple(range(8)), proportion=0.9, mutantID=8):
        """Create a sequential list of tuples of population objects running through each of the strategies defined,
        with a given proportion and a mutantID."""
        listOfStates = []
        mainProp = proportion
        mutantProp = round(1 - proportion, 3)
        for i in strategies:
            listOfStates.append((Population(ID=i, proportion=mainProp), Population(ID=mutantID, proportion=mutantProp)))
        listOfStates = tuple(listOfStates)
        return listOfStates

    @staticmethod
    def generateSinglePopulationProportionList(strategyID, mutantID):
        """Create a sequential list of population objects running through a single strategy with different
        proportions between it and the mutant strategy. Have to double check with population size to see if some
        decimal proportions lead to a non-integer number of agents with that strategy."""
        listOfStates = []
        strats = np.arange(1, 0, -0.05)
        strats = [round(strats[i], 3) for i in range(len(strats))]
        for i in strats:
            listOfStates.append((Population(ID=strategyID, proportion=i), Population(ID=mutantID,
                                                                                     proportion=round(1-i,3))))
        listOfStates = tuple(listOfStates)
        return listOfStates

    @staticmethod
    def generateSmallWorldParameters(nLower=2, nUpper=50, probabilityLower=0, probabilityUpper=1, nStep=10,
                                     probStep=0.1):
        """Iterate through both axes of initial degree (initialNeighbourCount) and the rewiringProbability to give a
        2-D plane of configurations"""
        smallWorldParams = []
        for n in np.arange(nLower, nUpper, nStep):
            for prob in np.arange(probabilityLower, probabilityUpper + 0.01, probStep):
                smallWorldParams.append((int(n), round(prob, 3)))
        return smallWorldParams

    def checkDensitiesForSize(self):
        """When changing the size of an ER Network if using sparseDensity flag, scan through all configs and correct
        the densities."""
        for config in self.experiments:
            size = config.size
            sparseDensity = 2 * np.log(size)/size
            if config.density != sparseDensity:
                logging.info(f'Changing density from {config.density} to {sparseDensity}.')
                config.density = sparseDensity


if __name__ == '__main__':
    C = Config(initialState=State(0, 1, 8), degree=5)
    # pops = Experiment.generatePopulationList(proportion=1, mutantID=8)
    # degs = [2, 3, 4, 5, 6]
    E = Experiment(
        networkType=LrGeRRLNetwork,
        variable='size',
        values=[100, 200],
        defaultConfig=C,
        repeats=2)
    E.showExperiments()
    E.run(export=True)

