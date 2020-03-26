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
        """Given a dictionary of counts of cooperators and defectors, append to network LocalData the proportions for that
         particular time period"""

        for key in actions:
            proportionAction = actions[key] / sum(actions.values())
            self.actions[key].append(proportionAction)

    @staticmethod
    def removeZeros(data):
        return NotImplementedError("removeZeros(data) function is removed")

    @classmethod
    def averageOverIterations(cls, iterations):
        """Take a dictionary where the key is the iteration number and each value is the corresponding pandas data-frame
         of LocalData. Return a single dataframe with averaged LocalData."""
        iterationsAsList = list(iterations.values())
        concatenatedResults = pd.concat(iterationsAsList, sort=False)
        byRowIndex = concatenatedResults.groupby(concatenatedResults.index)
        means = byRowIndex.mean()
        return means

    @staticmethod
    def initialiseOutputDirectory(experimentName):
        modulePath = os.path.dirname(os.path.realpath(__file__))
        resultsPath = os.path.join(modulePath, 'LocalData')
        os.mkdir(os.path.join(resultsPath, f'{experimentName}'))

    @staticmethod
    def exportResultsToCsv(experimentName, experimentConfig, experimentResults, experimentNumber):
        """Export the LocalData from a single data-frame averaged over many iterations as 'experimentName.csv' file"""

        modulePath = os.path.dirname(os.path.realpath(__file__))
        resultsPath = os.path.join(modulePath, 'LocalData')
        experimentPath = os.path.join(resultsPath, experimentName)
        fileName = f"{experimentNumber}.csv"
        experimentResults.to_csv(os.path.join(experimentPath, fileName))

    @staticmethod
    def exportExperimentConfigs(configsAsString, experimentName):
        """Export a text file containing all the configurations run into the same location as the LocalData."""
        fileName = "configs.txt"
        try:
            with open(fileName, 'w+') as c:
                c.write(configsAsString)
        except FileNotFoundError:
            print(configsAsString)

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

