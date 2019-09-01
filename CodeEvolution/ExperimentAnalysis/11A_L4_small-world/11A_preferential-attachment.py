from CodeEvolution.ExperimentAnalysis.analysis import *
"""
Experiment 11A-----------------------------------------------------------------------

    Finding the proportions of cooperation in watts-strogatz-small-world models, parameterised by rewiring
    probability alpha ranging from 0 (regular lattice) to 1 (fully random graph). (default 4 nearest neighbours,
    probability 0 -> 1 in steps of 0.1.

    Submitted: 08/24/2019 16:02:04
    11A_0   1582671
    11A_1   1582607
    11B_2   1632302
    11B_3   1632303
    11B_4   1632304
    11B_5   1632305
    11A_6   1582608
    11A_7   1582609
    
"""




if __name__ == '__main__':

    jobIDs = ['1582671', '1582607', '1632302','1632303','1632304','1632305', '1582608', '1582609']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]

    newXLabels = list(range(11))
    newXTicks = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]


    # Proportion of Cooperation
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    plt.title(f'LrGeER vs Rewiring Probability')
    plt.xlabel("Rewiring Probability")
    plt.ylabel("Average Final Proportion of Cooperation")
    plt.ylim(0.7, 0.9)
    plt.legend(loc='lower right')
    plt.xticks(newXLabels, newXTicks)
    plt.savefig("11A_rewiring-probability_cooperation")
    # plt.show()

    # Proportion of Strategies
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    plt.title(f'LrGeER vs Rewiring Probability')
    plt.xlabel("Rewiring Probability")
    plt.ylabel("Average Final Proportion of Strategies")
    plt.ylim(0.8, 1)
    plt.legend(loc='lower right')
    plt.xticks(newXLabels, newXTicks)
    plt.savefig("11A_rewiring-probability_proportion")
    # plt.show()



    #
    # for strategy, jobID in zip(strategyIDs, jobIDs):
    #     data = getDataFromID(jobID)
    #     fig, ax = plotCooperationProportion(data)
    #     plt.title(f'LrGeWSSW $s_{strategy}$ vs Rewiring Probability')
    #     plt.xlabel("$\\alpha$")
    #     plt.ylabel(f"Average Final Proportion of Cooperation")
    #     newLocs = list(range(11))
    #     newTicks = [round(i*0.1, 3) for i in range(11)]
    #     plt.xticks(ticks=newLocs, labels=newTicks)
    #     plt.savefig(jobID + "_cooperation")
    #     # plt.show()
