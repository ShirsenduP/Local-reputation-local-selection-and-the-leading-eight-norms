import pandas as pd
import os
import json

class Results():

    def __init__(self, config):
        self.strategies = {config.population.ID, config.mutant.ID}
        self.actions = {'C': [], 'D': []}
        self.strategyProportions = {}
        self.utilities = {}
        self.convergedAt = None

    def updateActions(self, actions):
        """Given a dictionary of counts of cooperators and defectors, append to network results the proportions for that
         particular time period"""

        for key in actions:
            proportionAction = actions[key]/sum(actions.values())
            self.actions[key].append(proportionAction)

    def exportUtilities(self):
        utils = self.removeZeros(self.utilities)
        utils = pd.DataFrame(utils).transpose()
        utils = utils.add_prefix('Average Util. Strategy #')
        return utils

    def exportActions(self):
        actions = pd.DataFrame(self.actions)
        actions = actions.rename(columns={'C': 'Prop. of Cooperators', 'D': 'Prop. of Defectors'})
        return actions

    def exportCensus(self):
        census = self.removeZeros(self.strategyProportions)
        census = pd.DataFrame(census).transpose()
        census = census.add_prefix('Prop. Strategy #')
        return census

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

    @classmethod
    def exportResultsToCSV(cls, experimentName, experimentConfig, experimentResults, experimentNumber):
        """Export the results from a single data-frame averaged over many iterations as 'experimentName.csv' file"""

        print('CURRENT DIR', os.getcwd())

        if 'results' not in os.listdir("CodeEvolution/"):
            os.mkdir(f"CodeEvolution/results/")

        if experimentName not in os.listdir("CodeEvolution/results"):
            os.mkdir(f"CodeEvolution/results/{experimentName}")

        experimentResults.to_csv(f"CodeEvolution/results/{experimentName}/{experimentNumber}.csv")

        def dumper(obj):
            return obj.__dict__

        with open(f"CodeEvolution/results/{experimentName}/{experimentNumber}.json", 'w') as f:
            f.write(json.dumps(experimentConfig, default=dumper, indent=4)) # use `json.loads` to do
            # the reverse

    def __str__(self):
        s = str(self.strategyProportions)
        s += 3*'\n'
        s += str(self.utilities)
        s += 3*'\n'
        s += str(self.actions)
        return s

