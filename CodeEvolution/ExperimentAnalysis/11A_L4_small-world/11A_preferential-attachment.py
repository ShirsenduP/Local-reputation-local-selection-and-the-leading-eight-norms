from CodeEvolution.ExperimentAnalysis.analysis import *
"""
Experiment 11A-----------------------------------------------------------------------

    Finding the proportions of cooperation in watts-strogatz-small-world models, parameterised by rewiring
    probability alpha ranging from 0 (regular lattice) to 1 (fully random graph). (default 4 nearest neighbours,
    probability 0 -> 1 in steps of 0.1.

    Submitted: 08/24/2019 16:02:04
    11A_0   1582671 - (1582606, 1582518)
    11A_1   1582607 - (1582519)
    11A_6   1582608 - (1582520)
    11A_7   1582609 - (1582521)
    
"""

if __name__ == '__main__':

    jobIDs = ['1582671', '1582607', '1582608', '1582609']
    strategyIDs = [0, 1, 6, 7]

    for strategy, jobID in zip(strategyIDs, jobIDs):
        data = getDataFromID(jobID)
        fig, ax = plotCooperationProportion(data)
        plt.title(f'LrGeWSSW $s_{strategy}$ vs Rewiring Probability')
        plt.xlabel("$\\alpha$")
        plt.ylabel(f"Average Final Proportion of Cooperation")
        newLocs = list(range(11))
        newTicks = [round(i*0.1, 3) for i in range(11)]
        plt.xticks(ticks=newLocs, labels=newTicks)
        plt.savefig(jobID + "_cooperation")
        # plt.show()
