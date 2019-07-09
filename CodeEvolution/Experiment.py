import time
import copy

import pandas as pd
from tqdm import trange

from CodeEvolution.GrGe import GrGe_Network
from CodeEvolution.LrLe import LrLe_Network
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
                setattr(tests[i], 'population', Population(ID=self.values[i][0].ID, proportion=self.values[i][
                    0].proportion))
                setattr(tests[i], 'mutant', Population(ID=self.values[i][1].ID, proportion=self.values[i][
                    1].proportion))
        else:
            # General Case
            tests = []
            for i in range(len(self.values)):
                newConfig = copy.deepcopy(self.default)
                tests.append(newConfig)
                setattr(tests[i], self.variable, self.values[i])

        self.experiments = tuple(tests)
        # print(self.experiments)

    def run(self, export=False, display=False, recordFull=False):
        """Run and export results for an experiment. This by default exports only the final state of the simulation,
        so the proportions of cooperators/defectors, the final proportions of each strategy. With the optional flag
        'recordFull', every time-step is recorded and then averaged. THIS IS NOT YET FULLY FUNCTIONAL as issues occur
         when multiple of the same parameterised run have different lengths of simulations."""

        experimentName = self.networkType.name + "_" + self.variable + "_" + time.strftime("%Y-%m-%d %H:%M")
        print("\nRunning ", experimentName, 50 * "=")
        if recordFull:
            raise NotImplementedError("Recording the full data releases data often incorrectly. Do not use.")

        if display:
            # pass
            print("Default Parameters:\t")
            print(self.default)

        def simulate(m_exp):
            # print(m_exp)
            N = self.networkType(m_exp)
            N.runSimulation()
            resultsActions = N.results.exportActions()
            resultsCensus = N.results.exportCensus()
            # resultsUtils = N.results.exportUtilities()
            # resultsFull = pd.concat([resultsActions, resultsCensus, resultsUtils], axis=1, sort=False)
            resultsFull = pd.concat([resultsActions, resultsCensus], axis=1, sort=False)
            return resultsFull.tail(1)

        for exp in trange(len(self.experiments), disable=display):
            if display:
                print(f"\nExperiment {exp} with {self.variable} at {self.values[exp]}")

            singleTest = pd.DataFrame()
            for _ in trange(self.repeats, leave=False, disable=display):
                singleRun = simulate(self.experiments[exp])
                singleTest = pd.concat([singleTest, singleRun], sort=False)

            if display:
                print(singleTest)
                print()

            if export:
                Results.exportResultsToCSV(experimentName, self.experiments[exp], singleTest, exp)

    @classmethod
    def generatePopulationList(cls, strategies=tuple(range(8)), proportion=0.9, mutantID=8):
        """Create a sequential list of Config objects running through each of the strategies defined, with a given
        proportion and a mutantID."""
        listOfStates = []
        mainProp = proportion
        mutantProp = round(1 - proportion, 3)
        for i in strategies:
            listOfStates.append((Population(ID=i, proportion=mainProp), Population(ID=mutantID, proportion=mutantProp)))
        listOfStates = tuple(listOfStates)
        return listOfStates


if __name__ == '__main__':
    pass

# TODO Need to change the experiment class so that it takes the different configs here too, GrGe/GrLe/etc

# TODO Check how the evolutionary update works in GrGe, looks a little funny, where is the counting the utilities and
#  interactions way? I think I am tracking the utilities this way in the utilityMonitor, but is not yet implemented
#  on the evolutionaryUpdate methods.

# TODO Find a way to let programs run through the night and then switch off when the script has finished running

# TODO Might need to swap the population/mutant input into two tuples..

# TODO Does probabilityOfMutants do anything?! -> YES! check mutation method, needs fix from todays meeting

# TODO keep track of the number of mutants added in random mutation

# TODO change the convergence condition to include epsilon ( probability of mutation )

# TODO final graphs get rid of the threshold, just average convergence point at the end of the simulation -> increase
#  the timesteps

# TODO plot the variation of convergence as we vary Tmax to see if it moves towards convergence - DO THIS FIRST

# TODO manager for Pycharm + Latex
#