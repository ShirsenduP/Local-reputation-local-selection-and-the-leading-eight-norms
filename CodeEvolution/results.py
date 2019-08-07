import logging

import pandas as pd
import os
import json


class Results:

    def __init__(self, config):
        self.strategies = {config.population.ID, config.mutant.ID}
        self.actions = {'C': [], 'D': []}
        self.strategyProportions = {}
        self.utilities = {}
        self.convergedAt = None
        self.mutantTracker = {}

    def updateActions(self, actions):
        """Given a dictionary of counts of cooperators and defectors, append to network results the proportions for that
         particular time period"""

        for key in actions:
            proportionAction = actions[key] / sum(actions.values())
            self.actions[key].append(proportionAction)

    def exportUtilities(self):
        # utils = self.removeZeros(self.utilities)
        utils = pd.DataFrame(self.utilities).transpose()
        utils = utils.add_prefix('Average Util. Strategy #')
        return utils

    def exportActions(self):
        actions = pd.DataFrame(self.actions)
        actions = actions.rename(columns={'C': 'Prop. of Cooperators', 'D': 'Prop. of Defectors'})
        return actions

    def exportCensus(self):
        # census = self.removeZeros(self.strategyProportions)
        census = pd.DataFrame(self.strategyProportions).transpose()
        census = census.add_prefix('Prop. Strategy #')
        return census

    def exportMutations(self):
        mutations = pd.Series(self.mutantTracker)
        mutations = mutations.rename("# of Mutants Added")
        return mutations

    @staticmethod
    def removeZeros(data):
        """Given a dictionary where each key is a time-step, and each corresponding value is another dictionary where the
        keys and values are the strategies and their average utilities, find the strategies that are not at the start
        of the simulation (as only two strategies are ever in play) and remove them from all time-steps."""
        emptyKeys = []
        nonEmptyKeys = []
        for key, value in data[0].items():
            if value == 0:
                emptyKeys.append(key)
            else:
                nonEmptyKeys.append(key)

        for key, value in data.items():
            for emptyKey in emptyKeys:
                data[key].pop(emptyKey, None)

        return data

    @classmethod
    def averageOverIterations(cls, iterations):
        """Take a dictionary where the key is the iteration number and each value is the corresponding pandas data-frame
         of results. Return a single dataframe with averaged results."""
        iterationsAsList = list(iterations.values())
        concatenatedResults = pd.concat(iterationsAsList, sort=False)
        byRowIndex = concatenatedResults.groupby(concatenatedResults.index)
        means = byRowIndex.mean()
        return means

    @staticmethod
    def initialiseOutputDirectory(experimentName):
        modulePath = os.path.dirname(os.path.realpath(__file__))
        resultsPath = os.path.join(modulePath, 'results')
        os.mkdir(os.path.join(resultsPath, f'{experimentName}'))

    @staticmethod
    def exportResultsToCsv(experimentName, experimentConfig, experimentResults, experimentNumber):
        """Export the results from a single data-frame averaged over many iterations as 'experimentName.csv' file"""

        modulePath = os.path.dirname(os.path.realpath(__file__))
        resultsPath = os.path.join(modulePath, 'results')
        experimentPath = os.path.join(resultsPath, experimentName)
        fileName = f"{experimentNumber}.csv"
        experimentResults.to_csv(os.path.join(experimentPath, fileName))

    @staticmethod
    def exportExperimentConfigs(configsAsString, experimentName):
        """Export a text file containing all the configurations run into the same location as the results."""
        modulePath = os.path.dirname(os.path.realpath(__file__))
        resultsPath = os.path.join(modulePath, 'results')
        experimentPath = os.path.join(resultsPath, experimentName)
        fileName = "configs.txt"
        configPath = os.path.join(experimentPath, fileName)
        with open(configPath, 'w') as c:
            c.write(configsAsString)

    @staticmethod
    def exportResultsToCsvCluster(experimentName, experimentConfig, experimentResults, experimentNumber):
        """Export data (.csv) into network storage"""

        direc = str(os.getcwd())+'/'
        experimentResults.to_csv(f"{direc}{experimentNumber}.csv", mode='w+')

    def __str__(self):
        s = str(self.strategyProportions)
        s += 3 * '\n'
        s += str(self.utilities)
        s += 3 * '\n'
        s += str(self.actions)
        return s

    # TODO: Move the census from Strategy class to Results class, makes more sense to track everything from here - IF
    #  IT AINT BROKE, DONT FIX IT!

