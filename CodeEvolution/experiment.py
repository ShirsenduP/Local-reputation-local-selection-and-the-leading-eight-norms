import logging
import os
import time
import copy

import numpy as np
import pandas as pd
from tqdm import trange
import json

from CodeEvolution.strategy import Strategy
from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork, LrLeERNetwork, LrGeRRLNetwork
from CodeEvolution.config import Config
from CodeEvolution.config import Population, State
from CodeEvolution.structures import RandomRegularLattice
from CodeEvolution.socialdilemna import MyEncoder


class Experiment:
    """This class generates a series of Config objects to run for a single experiment. Define a 'default' experiment,
     then choose (a SINGLE) variable to be varied, then add the list of values the variable will cycle through."""

    def __init__(self, networkType, description, variable=None, values=None, defaultConfig=Config(), repeats=100):
        self.networkType = networkType
        self.default = defaultConfig
        self.variable = variable
        self.values = values
        self.experiments = None
        self.repeats = repeats
        if defaultConfig.degree is not None:
            defaultConfig.density = None
        self.description = description
        self.generateConfigs()

    def run(self, export=False, expName=None):
        """Run and export LocalData for an experiment. This by default exports only the final state of the simulation,
        so the proportions of cooperators/defectors, the final proportions of each strategy. With the optional flag
        'recordFull', every time-step is recorded and then averaged. THIS IS NOT YET FULLY FUNCTIONAL as issues occur
         when multiple of the same parameterised run have different lengths of simulations. Cluster takes precedence
         over export."""

        if expName:
            experimentName = expName
        else:
            experimentName = self.variable

        results = pd.DataFrame(dtype='float64')

        # run all tests in the experiment
        for exp in trange(len(self.experiments)):

            single_Test = pd.DataFrame(dtype='float64')
            for _ in range(self.repeats):
                # Run a single simulation
                N = self.networkType(self.experiments[exp])
                single_Run = N.runSimulation()

                # If population is being tested, the self.variable is unnecessary
                if self.variable != 'population':
                    single_Run[self.variable] = self.values[exp]

                # Add the simulation onto dataframe of completed sims
                single_Test = pd.concat([single_Test, single_Run], axis=1, sort=False)
            single_Test = single_Test.transpose()
            results = pd.concat([results, single_Test], axis=0, sort=False)

        if export:
            # Export Results DataFrame to csv
            results.to_csv(experimentName+'.csv', index=True, header=True)

            # Export experiment configs to txt file
            with open(f"{experimentName}.txt", "w+") as f:
                f.write(self.description)
                f.write(10*"=="+2*"\n")
                for config in self.experiments:
                    f.write(json.dumps(config.__dict__, cls=MyEncoder))
                    f.write(2*"\n")
            return results
        else:
            return results

    def generateConfigs(self):
        """Given a variable and the range of values to be tested for that variable, _generate a list of Config objects
        for each of those tests"""
        if self.variable is None or self.values is None:
            raise ValueError(
                "Parameters 'variable' and 'values' must not be None.")

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
        if self.default.degree is not None or self.variable == 'degree':
            self.assignNewDensitiesFromDegree(tests)

        self.experiments = tuple(tests)

    def showExperiments(self, asString=False):
        """Print to the console a condensed list of all the config files in the object's experiment list."""
        s = str()
        for thing in self.experiments:
            s += str(thing.__dict__) + 2 * "\n"

        if asString:
            return s
        else:
            print(s)

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
    def generatePopulationList(strategies=tuple(range(8)), proportion=0.9, mutantID=8):
        """Create a sequential list of tuples of population objects running through each of the strategies defined,
        with a given proportion and a mutantID."""
        listOfStates = []
        mainProp = proportion
        mutantProp = round(1 - proportion, 3)
        for i in strategies:
            listOfStates.append((Population(ID=i, proportion=mainProp), Population(
                ID=mutantID, proportion=mutantProp)))
        listOfStates = tuple(listOfStates)
        return listOfStates

    @staticmethod
    def generateSinglePopulationProportionList(strategyID, mutantID):
        """Create a sequential list of population objects running through a single strategy with different
        proportions between it and the mutant strategy. Have to double check with population size to see if some
        decimal proportions lead to a non-integer number of agents with that strategy."""
        listOfStates = []
        strats = np.arange(1, 0, -0.25)
        strats = [round(strats[i], 3) for i in range(len(strats))]
        for i in strats:
            listOfStates.append((Population(ID=strategyID, proportion=i), Population(ID=mutantID,
                                                                                     proportion=round(1-i, 3))))
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
                logging.info(
                    f'Changing density from {config.density} to {sparseDensity}.')
                config.density = sparseDensity
