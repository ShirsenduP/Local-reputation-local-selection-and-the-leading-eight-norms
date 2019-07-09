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
        """Given the name of the experiment run (the name of the directory within the results subdirectory where the
        results are saved.) this class will plot all results automatically."""

        resultsDir = os.getcwd() + "/results/" + str(name)
        dataFiles = [filepath for filepath in os.listdir(resultsDir) if ".csv" in filepath]
        configFiles = [filepath for filepath in os.listdir(resultsDir) if ".json" in filepath]

        dataFiles.sort()
        configFiles.sort()

        dataDict = {}
        index = 0
        for file in dataFiles:
            with open(resultsDir + "/" + file) as f:
                dataDict[index] = pd.read_csv(f)
                index += 1

        return dataDict

    @staticmethod
    def show_result_dir():
        """Print a list of the results directory where the outputs of each experiment are saved."""
        resultsDir = os.getcwd() + "/results/"
        resultsPath = os.listdir(resultsDir)
        resultsPath.sort()
        print("Results Directory\n".upper())
        for test in resultsPath:
            print(test)

    @staticmethod
    def getStrategyLabels():
        labelForGraphs = list(range(8))
        for i in range(len(labelForGraphs)):
            labelForGraphs[i] = "$s_{" + str(labelForGraphs[i]) + "}$"
        return labelForGraphs

    @staticmethod
    def getProportionOfStable(data, threshold=0.75):
        """Given a dictionary of data-frames consisting of every population vs All-D, calculate the proportion of
        times the main population remains an Evolutionary Stable Strategy (ESS)."""

        # Number of strategies tested in the dictionary
        nStrategies = len(data.keys())
        output = []
        for strategy in range(nStrategies):
            # Get the data for the i'th strategy
            df = data[strategy]
            columnName = 'Prop. Strategy #' + str(strategy)
            total = len(df)

            # Calculate the proportion of times the final proportion of the strategy is above the threshold
            stable = df[df[columnName] >= threshold]
            # unstable = df[df[columnName] < threshold]
            proportionStable = len(stable) / total
            # proportionUnstable = len(unstable) / total

            output.append(proportionStable)

        return output


if __name__ == "__main__":
    pass
