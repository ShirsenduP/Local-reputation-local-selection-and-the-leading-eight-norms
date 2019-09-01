"""
Experiment 10A

Effect of increasing the mutation rate on LrGeERNetwork to see where the threshold is for mutation to dominate
Range from 0.1, 0.5 - 10 in 0.5 increments. Recall this parameter represents the expected number of mutations/time-step.

    10A_0   1574518
    10A_1   1574519
    10B_2   1632729
    10B_3   1632730
    10B_4   1632731
    10B_5   1632732
    10A_6   1574520
    10A_7   1574521

"""

from CodeEvolution.ExperimentAnalysis.analysis import *

if __name__ == '__main__':

    jobIDs = ['1574518', '1574519', '1632729', '1632730', '1632731', '1632732', '1574520', '1574521']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]

    newXTicks = list(range(0, 11))
    newXLabels = list(np.arange(0, 11, 1))

    # Proportion of Cooperation
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    plt.title(f'LrGeER vs Max Length of Simulation')
    plt.xlabel("Mutation Rate")
    plt.ylabel("Average Final Proportion of Cooperation")
    plt.legend(loc='upper right')
    plt.xticks(newXLabels, newXTicks)
    plt.savefig("10A_mutationrate-cooperation")
    # plt.show()

    # Proportion of Strategies
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    plt.title(f'LrGeER vs Max Length of Simulation')
    plt.xlabel("Mutation Rate")
    plt.ylabel("Average Final Proportion of Strategies")
    plt.legend(loc='upper right')
    plt.xticks(newXLabels, newXTicks)
    plt.savefig("10A_mutationrate-proportion")
    # plt.show()

