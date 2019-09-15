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
    strategyIDs = list(range(8))
    skip = [2, 3, 4, 5]

    # plotAllStrategyProportions(jobIDs, list(range(8)), skip)
    # plt.title('LrGeRRL vs RRL Degree')
    # newXLocs = list(range(3, 14))
    # newXTicks = list(range(11))
    # plt.xlabel("RRL Degree $d$")
    # plt.ylabel(f"Average Final Strategy Proportion")
    # plt.xticks(newXTicks, newXLocs)
    # plt.legend(bbox_to_anchor=(0.85,0.7))
    # # plt.savefig('6A_proportion')
    # plt.show()
    #
    # plotAllStrategyCooperations(jobIDs, list(range(8)), skip)
    # plt.title('LrGeRRL vs RRL Degree')
    # newXLocs = list(range(3, 14))
    # newXTicks = list(range(11))
    # plt.xlabel("RRL Degree $d$")
    # plt.ylabel(f"Average Proportion of Cooperation")
    # plt.xticks(newXTicks, newXLocs)
    # plt.legend()
    # # plt.savefig('6A_cooperation')
    # # plt.show()

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all')
    # labels = [f'$s_{strategyID}$' for strategyID in strategyIDs if strategyID not in skip]
    xlabels = list(range(3, 14))
    xticks = list(range(11))

    plt.sca(ax1)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabels)
    ax1.set_ylabel("Prop. of \nStrategy")

    plt.sca(ax2)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xlabels)
    ax2.set_xlabel('$d$')
    ax2.set_ylabel("Prop. of \nCooperators")

    handles, labels = ax2.get_legend_handles_labels()
    lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    plt.savefig('6A_l4-rrl', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()