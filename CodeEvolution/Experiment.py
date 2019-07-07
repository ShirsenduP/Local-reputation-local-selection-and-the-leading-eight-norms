import time
from pprint import pprint

import pandas as pd
from tqdm import trange

from CodeEvolution.GrGe import GrGe_Network
from CodeEvolution.LrGe import LrGe_Network
from CodeEvolution.LrLe import LrLe_Network
from CodeEvolution.config import Config
from CodeEvolution.config import Population
from CodeEvolution.results import Results


class Experiment:
    """This class generates a series of Config objects to run for a single experiment. Define a 'default' experiment,
     then choose (a SINGLE) variable to be varied, then add the list of values the variable will cycle through."""

    def __init__(self, networkType, variable=None, values=None, defaultConfig=Config(), repeats=1):
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
        tests = []
        for i in range(len(self.values)):
            tests.append(Config())
            setattr(tests[i], self.variable, self.values[i])
        self.experiments = tuple(tests)

    def run(self, export=False, display=False, recordFull=False):
        """Run and export results for an experiment. This by default exports only the final state of the simulation,
        so the proportions of cooperators/defectors, the final proportions of each strategy. With the optional flag
        'recordFull', every time-step is recorded and then averaged. THIS IS NOT YET FULLY FUNCTIONAL as issues occur
         when multiple of the same parameterised run have different lengths of simulations."""

        networkType = type(self.networkType).__name__.replace("_Network", "")
        experimentName = networkType + "_" + self.variable + "_" + time.strftime("%Y-%m-%d %H:%M")
        print(experimentName)
        if recordFull:
            raise NotImplementedError("Recording the full data releases data often incorrectly. Do not use.")

        if display:
            print("DEFAULT PARAMETERS\n")
            pprint(self.default)

        def simulate(m_exp):
            N = GrGe_Network(m_exp)
            N.runSimulation()
            resultsActions = N.results.exportActions()
            resultsCensus = N.results.exportCensus()
            # resultsUtils = N.results.exportUtilities()
            # resultsFull = pd.concat([resultsActions, resultsCensus, resultsUtils], axis=1, sort=False)
            resultsFull = pd.concat([resultsActions, resultsCensus], axis=1, sort=False)
            return resultsFull.tail(1)

        for exp in trange(len(self.experiments)):
            if display:
                print(f"\nExperiment {exp} with {self.variable} at {self.values[exp]}")

            singleTest = pd.DataFrame()
            for rep in trange(self.repeats, leave=False):
                singleRun = simulate(self.experiments[exp])
                singleTest = pd.concat([singleTest, singleRun], sort=False)

            if display:
                print(singleTest)

            if export:
                Results.exportResultsToCSV(experimentName, self.experiments[exp], singleTest, exp)

    @classmethod
    def generatePopulationList(cls):
        """Create a sequential list of Config objects running through all the populations at a given proportion 0.9."""
        configs = []
        for i in range(8):
            configs.append(Population(ID=i, Proportion=0.9))
        return configs


if __name__ == '__main__':

    pops = Experiment.generatePopulationList()
    reps = 3
    """All-D versus all the populations, initially weighted at 10/90."""

    # default = Config(densities=1, mutant=Population(ID=8, Proportion=0.1))
    # E = Experiment(networkType=GrGe_Network, defaultConfig=default, variable='population', values=pops, repeats=reps)
    # E.run(export=True)
    #
    # default2 = Config(densities=0.1)
    # E2 = Experiment(networkType=LrGe_Network, defaultConfig=default2, variable='population', values=pops, repeats=reps)
    # E2.run(export=True)
    #
    # default3 = Config(densities=0.1)
    # E3 = Experiment(networkType=LrLe_Network, defaultConfig=default3, variable='population', values=pops, repeats=reps)
    # E3.run(export=True)
    #
    # """All-C versus all the populations, initially weighted at 10/90."""
    #
    # default4 = Config(densities=1, mutant=Population(ID=9, Proportion=0.1))
    # E = Experiment(networkType=GrGe_Network, defaultConfig=default4, variable='population', values=pops, repeats=reps)
    # E.run(export=True)
    #
    # default5 = Config(densities=0.1, mutant=Population(ID=9, Proportion=0.1))
    # E2 = Experiment(networkType=LrGe_Network, defaultConfig=default5, variable='population', values=pops, repeats=reps)
    # E2.run(export=True)

    default6 = Config(densities=0.1, mutant=Population(ID=9, Proportion=0.1))
    E3 = Experiment(networkType=LrLe_Network, defaultConfig=default6, variable='population', values=pops, repeats=reps)
    E3.run(display=True)

# TODO Need to change the experiment class so that it takes the different configs here too, GrGe/GrLe/etc

# TODO Check how the evolutionary update works in GrGe, looks a little funny, where is the counting the utilities and
#  interactions way? I think I am tracking the utilities this way in the utilityMonitor, but is not yet implemented
#  on the evolutionaryUpdate methods.

# TODO Find a way to let programs run through the night and then switch off when the script has finished running

# TODO Add a nickname to the Experiment class to prepend onto experiment names cos the type(class) isn't working
