import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.style
import matplotlib as mpl

mpl.style.use('seaborn')


class Evaluator:

    @staticmethod
    def open_results(name):
        """Given the name of the experiment run (the name of the directory within the LocalData subdirectory where the
        LocalData are saved.) this class will plot all LocalData automatically."""

        # resultsDir = os.getcwd() + "/LocalData/" + str(name)
        # dataFiles = [filepath for filepath in os.listdir(resultsDir) if ".csv" in filepath]
        # configFiles = [filepath for filepath in os.listdir(resultsDir) if ".json" in filepath]
        #
        # dataFiles.sort()
        # configFiles.sort()
        #
        # dataDict = {}
        # index = 0
        # for file in dataFiles:
        #     with open(resultsDir + "/" + file) as f:
        #         dataDict[index] = pd.read_csv(f)
        #         index += 1
        #
        # return dataDict
        raise NotImplementedError("Evaluator.py methods have been removed.")

    @staticmethod
    def show_result_dir():
        """Print a list of the LocalData directory where the outputs of each experiment are saved."""
        # resultsDir = os.getcwd() + "/LocalData/"
        # resultsPath = os.listdir(resultsDir)
        # resultsPath.sort()
        # print("Results Directory\n".upper())
        # for test in resultsPath:
        #     print(test)
        raise NotImplementedError("Evaluator.py methods have been removed.")

    @staticmethod
    def getStrategyLabels():
        # labelForGraphs = list(range(8))
        # for i in range(len(labelForGraphs)):
        #     labelForGraphs[i] = "$s_{" + str(labelForGraphs[i]) + "}$"
        # return labelForGraphs
        raise NotImplementedError("Evaluator.py methods have been removed.")

    @staticmethod
    def getProportionOfStable(data, threshold=0.75):
        """Given a dictionary of data-frames consisting of every population vs All-D, calculate the proportion of
        times the main population remains an Evolutionary Stable Strategy (ESS)."""

        # # Number of strategies tested in the dictionary
        # nStrategies = len(data.keys())
        # output = []
        # for strategy in range(nStrategies):
        #     # Get the data for the i'th strategy
        #     df = data[strategy]
        #     columnName = 'Prop. Strategy #' + str(strategy)
        #     total = len(df)
        #
        #     # Calculate the proportion of times the final proportion of the strategy is above the threshold
        #     stable = df[df[columnName] >= threshold]
        #     # unstable = df[df[columnName] < threshold]
        #     proportionStable = len(stable) / total
        #     # proportionUnstable = len(unstable) / total
        #
        #     output.append(proportionStable)
        #
        # return output
        raise NotImplementedError("Evaluator.py methods have been removed.")

    @staticmethod
    def plotAllStrategies(title, dataPath, mutantID, save=False):
        """Given the name of an experiment in the LocalData directory, plot the data in a scatterplot where each point
        represents a single simulation with the (x,y) coordinate representing (timestep at convergence,
        final proportion of mutants)."""

        # data = Evaluator.open_results(dataPath)
        # strategyID = iter(range(len(data)))
        #
        # for strategy in data.values():
        #     x = strategy['Unnamed: 0']
        #     y = strategy[f'Prop. Strategy #{mutantID}']
        #     seriesID = next(strategyID)
        #     plt.scatter(x, y, label=str(seriesID), marker=seriesID, s=40, alpha=0.3)
        #
        # plt.title(title)
        # plt.xlabel('Time-steps to convergence')
        # plt.ylabel('Final proportion of Mutants')
        # plt.legend(loc='center left')
        # if save:
        #     resultsDir = os.getcwd() + '/LocalData/' + dataPath + '/' + title
        #     plt.savefig(resultsDir)
        # else:
        #     plt.show()
        raise NotImplementedError("Evaluator.py methods have been removed.")

    @staticmethod
    def plotAllStrategiesSummary(title, dataPath, mutantID, save=False):
        """Given the name of an experiment in the LocalData directory, plot the means of the proportions of mutants
        amongst each strategy along with error bars. Optionally save plot as .png in dataPath directory."""

        # data = Evaluator.open_results(dataPath)
        # strategies = list(range(8))
        # mean = [datum[f'Prop. Strategy #{mutantID}'].mean() for datum in data.values()]
        # dev = [datum[f'Prop. Strategy #{mutantID}'].std() for datum in data.values()]
        #
        # fig, ax = plt.subplots()
        # ax.errorbar(strategies, mean,
        #             yerr=dev,
        #             ecolor='grey',
        #             solid_capstyle='projecting',
        #             capsize=5,
        #             elinewidth=2,
        #             markeredgewidth=2)
        #
        # plt.rcParams.update({'font.size': 40})
        # plt.title(title)
        # plt.xlabel("Strategy ID")
        # plt.ylabel(f"Final proportion of Mutants {mutantID}")
        #
        # if save:
        #     resultsDir = os.getcwd() + '/LocalData/' + dataPath + '/' + dataPath
        #     plt.savefig(resultsDir)
        # else:
        #     plt.show()
        raise NotImplementedError("Evaluator.py methods have been removed.")

if __name__ == "__main__":
    pass
