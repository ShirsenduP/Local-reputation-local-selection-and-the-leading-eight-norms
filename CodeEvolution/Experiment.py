import pandas as pd
import time

from CodeEvolution.config import Config
from CodeEvolution.GrGe import GrGe_Network
from CodeEvolution.config import Population
from CodeEvolution.results import Results

class Experiment:
    """This class generates a series of Config objects to run for a single experiment. Define a 'default' experiment,
     then choose (a SINGLE) variable to be varied, then add the list of values the variable will cycle through."""

    def __init__(self, variable=None, values=None, defaultConfig=Config(), repeats=1):
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

        if recordFull:
            raise NotImplementedError("Recording the full data releases data but often incorrectly. Do not use.")

        if display:
            print("DEFAULT PARAMETERS")
            print(self.default)

        experimentResults = []
        for exp in range(len(self.experiments)):

            if display:
                print(f"Experiment {exp} with {self.variable} at {self.values[exp]}")

            singleTest = pd.DataFrame()

            for rep in range(self.repeats):
                def simulate(m_exp):
                    N = GrGe_Network(m_exp)
                    N.runSimulation()
                    resultsActions = N.results.exportActions()
                    resultsCensus = N.results.exportCensus()
                    # resultsUtils = N.results.exportUtilities()
                    # resultsFull = pd.concat([resultsActions, resultsCensus, resultsUtils], axis=1, sort=False)
                    resultsFull = pd.concat([resultsActions, resultsCensus], axis=1, sort=False)
                    return resultsFull.tail(1)
                singleRun = simulate(self.experiments[exp])
                singleTest = pd.concat([singleTest, singleRun], sort=False)

            if display:
                print(singleTest)

            if export:
                experimentName = self.variable + "__" + time.strftime("%Y-%m-%d %H:%M")
                Results.exportResultsToCSV(experimentName, self.experiments[exp], singleTest, exp)


if __name__=='__main__':
    default = Config(size=100, maxPeriods=500)
    E = Experiment(defaultConfig=default, variable='density', values=[0.05, 0.1, 0.15, 0.2, 0.25, 0.3], repeats=3)

    E.run(display=True, export=True)
    # print(R)

