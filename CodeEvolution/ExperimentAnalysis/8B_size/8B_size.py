from CodeEvolution.ExperimentAnalysis.analysis import *

"""
Experiment 8B-----------------------------------------------------------------------

Effect of size of network on the number of leading strategies for Local Reputation,
Global Evolution and an Erdos Renyi network.

	8B.0    1746310
	8B.1    1746316
	8B.2    1746320
	8B.3    1746323
	8B.4    1748536
	8B.5    1748537
	8B.6    1748538
	8B.7    1748539


"""



if __name__ == '__main__':
    jobIDs = ['1746310', '1746316', '1746320', '1746323', '1748536', '1748537', '1748538', '1748539']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = []

    # plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    # plt.title(f'LrGeER vs Size of Network')
    # plt.xlabel("$n$ Agents")
    # plt.ylabel(f"Average Final Proportion of Strategy")
    xticks, xlabels = range(0, 10, 1), list(range(50, 550, 50))
    # plt.legend(loc='best')
    # plt.xticks(xpos, xticks, rotation=45)
    # # plt.savefig("8B_size_strategy-proportion")
    # plt.show()
    #
    # plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    # plt.title(f'LrGeER vs Size of Network')
    # plt.xlabel("$T_{max}$")
    # plt.ylabel("Average Final Proportion of Cooperation")
    # xpos, xticks = range(0, 10, 1), list(range(50, 550, 50))
    # plt.legend(loc='best')
    # plt.xticks(xpos, xticks, rotation=45)
    # # plt.savefig("8B_size_cooperation-proportion")
    # plt.show()
    #
    #
    #

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all')
    # labels = [f'$s_{strategyID}$' for strategyID in strategyIDs if strategyID not in skip]

    plt.sca(ax1)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabels)
    ax1.set_ylabel("Prop. of \nStrategy")

    plt.sca(ax2)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xlabels)
    ax2.set_xlabel('Size of Network $n$')
    ax2.set_ylabel("Prop. of \nCooperators")

    handles, labels = ax2.get_legend_handles_labels()
    lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    plt.savefig('8B_size', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()
