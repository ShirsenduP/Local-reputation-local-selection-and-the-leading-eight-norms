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
    # show_result_dir()

    GrGe_AllD = Evaluator.open_results("type_population_2019-07-07 00:48")
    LrGe_AllD = Evaluator.open_results("type_population_2019-07-07 01:32")
    LrLe_AllD = Evaluator.open_results("type_population_2019-07-07 02:15")
    GrGe_AllC = Evaluator.open_results("type_population_2019-07-07 03:00")
    LrGe_AllC = Evaluator.open_results("type_population_2019-07-07 03:45")
    LrLe_AllC = Evaluator.open_results("type_population_2019-07-07 04:30")

    # Need to look at Simone's paper to see ideas for graphs

    GrGe_AllD_Stable_Proportion = Evaluator.getProportionOfStable(GrGe_AllD)
    GrGe_AllC_Stable_Proportion = Evaluator.getProportionOfStable(GrGe_AllC)
    LrGe_AllD_Stable_Proportion = Evaluator.getProportionOfStable(LrGe_AllD)
    LrGe_AllC_Stable_Proportion = Evaluator.getProportionOfStable(LrGe_AllC)
    LrLe_AllD_Stable_Proportion = Evaluator.getProportionOfStable(LrLe_AllD)
    LrLe_AllC_Stable_Proportion = Evaluator.getProportionOfStable(LrLe_AllC)

    labels = Evaluator.getStrategyLabels()
    x = np.arange(len(labels))
    width = 0.13

    # fig = plt.figure()
    fig, ax = plt.subplots(figsize=(10,3))

    rects1A = ax.bar(x - 5 * width / 2, GrGe_AllD_Stable_Proportion, width, label='GrGe_All-D')
    rects1B = ax.bar(x - 3 * width / 2, GrGe_AllC_Stable_Proportion, width, label='GrGe_All-C')

    rects2A = ax.bar(x - 1 * width / 2, LrGe_AllD_Stable_Proportion, width, label='LrGe_All-D')
    rects2B = ax.bar(x + 1 * width / 2, LrGe_AllC_Stable_Proportion, width, label='LrGe_All-C')

    rects3A = ax.bar(x + 3 * width / 2, LrLe_AllD_Stable_Proportion, width, label='LrLe_All-D')
    rects3B = ax.bar(x + 5 * width / 2, LrLe_AllC_Stable_Proportion, width, label='LrLe_All-C')

    ax.set_title('Proportions of the leading eight that remain stable against All-C/D')
    ax.set_xticks(x)
    ax.set_ylabel('Proportion of Simulations \nwith stable strategy')

    ax.set_xticklabels(labels)
    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 - box.height * 0.15, box.width, box.height * 1.2])

    fig.legend(loc='lower center', bbox_to_anchor=(0.5, 0.03), fancybox=True, shadow=True, ncol=6)
    plt.show()
    fig.savefig('Leading8_density_too_high')
