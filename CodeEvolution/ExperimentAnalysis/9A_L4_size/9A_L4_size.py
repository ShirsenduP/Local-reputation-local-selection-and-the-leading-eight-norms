from CodeEvolution.ExperimentAnalysis.analysis import *

"""
Experiment 9A-----------------------------------------------------------------------

Effect of simulation on variance of convergence point, Erdos Renyi network, size 300, test maxT from 500-5000 at
intervals of 250 to see if maxT of 5000 is necessary for every simulation.

    9A_0    1582527
    9A_1    1576515
    9B_2    1633286
    9B_3    1633287
    9B_4    1633288
    9B_5    1633289
    9A_6    1574515
    9A_7    1574516

"""

if __name__ == '__main__':
    jobIDs = ['1582527', '1576515', '1633286', '1633287', '1633288', '1633289', '1574515', '1574516']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = []

    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    plt.title(f'LrGeER vs Max Length of Simulation')
    plt.xlabel("$T_{max}$")
    plt.ylabel(f"Average Final Proportion of Strategy")
    xpos, xticks = range(0, 20, 2), list(range(500, 5001, 500))
    plt.legend(loc='lower right')
    plt.xticks(xpos, xticks, rotation=45)
    # plt.savefig("9A_Tmax_strategy-proportion")
    # plt.show()

    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    plt.title(f'LrGeER vs Max Length of Simulation')
    plt.xlabel("$T_{max}$")
    plt.ylabel("Average Final Proportion of Cooperation")
    xpos, xticks = range(0, 20, 2), list(range(500, 5001, 500))
    plt.legend(loc='lower right')
    plt.xticks(xpos, xticks, rotation=45)
    # plt.savefig("9A_Tmax_cooperation")
    # plt.show()