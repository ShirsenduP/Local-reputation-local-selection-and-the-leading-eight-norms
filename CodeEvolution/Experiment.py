import logging
import os
import time
import copy

import numpy as np
import pandas as pd
from tqdm import trange

from CodeEvolution import Strategy
from CodeEvolution.models import GrGeNetwork, LrGeNetwork, LrLeNetwork
from CodeEvolution.config import Config
from CodeEvolution.config import Population, State
from CodeEvolution.results import Results


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

        self.experiments = tuple(tests)
        # print(self.experiments)

    @staticmethod
    def generateParameterFile(defaultConfig, variable, values, repeats):
        """Export a parameters file (.txt) for UCL clusters"""

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
        N = networkType(m_exp)
        # print(N)
        N.runSimulation()
        resultsActions = N.results.exportActions()
        resultsCensus = N.results.exportCensus()
        # print(resultsCensus)
        # if (resultsCensus>1).any():
        #     logging.critical("Census thinks there are more agents than there are.")
        resultsUtils = N.results.exportUtilities()
        resultsMutations = N.results.exportMutations()
        resultsFull = pd.concat([resultsCensus, resultsActions, resultsUtils, resultsMutations], axis=1, sort=False)
        resultsFull['# of Mutants Added'].iloc[-1:] = resultsFull['# of Mutants Added'].sum()
        if displayFull:
            print(resultsFull)
        # Rename index
        resultsFull.index.names = ['Tmax']
        return resultsFull.tail(1)

    def run(self, export=False, display=False, recordFull=False, displayFull=False, cluster=False):
        """Run and export results for an experiment. This by default exports only the final state of the simulation,
        so the proportions of cooperators/defectors, the final proportions of each strategy. With the optional flag
        'recordFull', every time-step is recorded and then averaged. THIS IS NOT YET FULLY FUNCTIONAL as issues occur
         when multiple of the same parameterised run have different lengths of simulations. Cluster takes precedence
         over export."""

        experimentName = self.networkType.name + "_" + self.variable + "_" + time.strftime("%Y-%m-%d %H:%M:%S")

        print("\nRunning ", experimentName, 50 * "=")
        if recordFull:
            raise NotImplementedError("Recording the full data releases data often incorrectly. Do not use.")

        for exp in trange(len(self.experiments), leave=False):
            if display:
                print(f"\nExperiment {exp} with {self.variable} at {self.values[exp]}")

            singleTest = pd.DataFrame()
            for _ in trange(self.repeats, leave=False):
                Strategy.reset()
                singleRun = self.simulate(self.experiments[exp], self.networkType, displayFull)
                singleTest = pd.concat([singleTest, singleRun], sort=False)
                Strategy.reset()

            # if cluster:
            #     singleTest.to_csv(f"{exp}", mode='w')

            if display:
                print()
                print(singleTest)
                print()

            if cluster:
                # If multiple experiments run from the same script, the data files will overwrite previous files with
                # same names
                Results.exportResultsToCsvCluster(experimentName, self.experiments[exp], singleTest, exp)
            elif export:
                Results.exportResultsToCsv(experimentName, self.experiments[exp], singleTest, exp)

    def showExperiments(self):
        """Print to the console a condensed list of all the config files in the object's experiment list."""
        for thing in self.experiments:
            print(thing.__dict__)

    @classmethod
    def generatePopulationList(cls, strategies=tuple(range(8)), proportion=0.9, mutantID=8):
        """Create a sequential list of tuples of population objects running through each of the strategies defined,
        with a given proportion and a mutantID."""
        listOfStates = []
        mainProp = proportion
        mutantProp = round(1 - proportion, 3)
        for i in strategies:
            listOfStates.append((Population(ID=i, proportion=mainProp), Population(ID=mutantID, proportion=mutantProp)))
        listOfStates = tuple(listOfStates)
        return listOfStates


if __name__ == '__main__':
    C = Config(initialState=State(0, 1, 8), size=500, sparseDensity=True)
    pops = Experiment.generatePopulationList(strategies=(range(4),), proportion=1, mutantID=8)
    E = Experiment(
        networkType=GrGeNetwork,
        variable='population',
        values=pops,
        defaultConfig=C)
    E.generateParameterFile(
        defaultConfig=Config(),
        variable='density',
        values=list(np.linspace(0.01, 1, 10)),
        repeats=10
        )

# TODO IF FILES ALREADY EXIST IN DIRECTORY, CREATE NEW FOLDER - DO NOT OVERWRITE THIS IS BLOODY ANNOYING

# TODO LOGGING NEEDED URGENTLY for each interaction

# TODO FIRST TEST final graphs get rid of the threshold, just average convergence point at the end of the simulation ->
#  increase
#  the timesteps

# TODO plot the variation of convergence as we vary Tmax to see if it moves towards convergence - DO THIS FIRST

# TODO Let Prisoners dilemma class be serializable

# TODO Find a way to let programs run through the night and then switch off when the script has finished running


# TODO TESTS
"""	1. starting 50/50 mutants and some Strategy
    2. Initially a strategy and no mutants - at the end of each timestep, each agent has some 'probabilityOfMutants'
     of turning into a mutant (<< .1 )
    3. test the number of mutants needed to kill the system"""
