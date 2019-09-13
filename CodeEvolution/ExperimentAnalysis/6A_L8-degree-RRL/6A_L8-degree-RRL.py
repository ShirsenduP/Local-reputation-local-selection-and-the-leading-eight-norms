"""
Experiment 6A

Effect of degree of regular random lattice on proportions of cooperation
Strategy i = [0,7] vs degree d [13, 3]

    6A_0    1557510
    6A_1    1557511
    6A_2    1536574
    6A_3    1536575
    6A_4    1536576
    6A_5    1536577
    6A_6    1557512
    6A_7    1560446

"""

from CodeEvolution.ExperimentAnalysis.analysis import *

if __name__ == '__main__':
    jobIDs = ['1557510', '1557511', '1536574', '1536575', '1536576', '1536577', '1557512', '1560446']
    # skip = []
    skip = [2, 3, 4, 5]

    plotAllStrategyProportions(jobIDs, list(range(8)), skip)
    plt.title('LrGeRRL vs RRL Degree')
    newXLocs = list(range(3, 14))
    newXTicks = list(range(11))
    plt.xlabel("RRL Degree $d$")
    plt.ylabel(f"Average Final Strategy Proportion")
    plt.xticks(newXTicks, newXLocs)
    plt.legend(bbox_to_anchor=(0.85,0.7))
    # plt.savefig('6A_proportion')
    plt.show()

    plotAllStrategyCooperations(jobIDs, list(range(8)), skip)
    plt.title('LrGeRRL vs RRL Degree')
    newXLocs = list(range(3, 14))
    newXTicks = list(range(11))
    plt.xlabel("RRL Degree $d$")
    plt.ylabel(f"Average Proportion of Cooperation")
    plt.xticks(newXTicks, newXLocs)
    plt.legend()
    # plt.savefig('6A_cooperation')
    # plt.show()
