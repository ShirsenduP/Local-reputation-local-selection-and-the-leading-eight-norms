from CodeEvolution.ExperimentAnalysis.analysis import *

"""
Experiment 12ABC-----------------------------------------------------------------------

    Allowing no mutation, but modulating the initial proportion of mutants in the population to find the limiting point
    of where the network can recover. Range 0-1 in 0.05 increments.

Experiment 12A - INCOMPLETE
    Erdos Renyi
    12A_0   1748690
    12A_1   1748691
    12A_6   1748692
    12A_7   1748693

Experiment 12B - DONE

    Scale-Free (preferential attachment parameter 2)
    12B_0   1748699
    12B_1   1749037
    12B_6   1749038
    12B_7   1749039

Experiment 12C - DONE

    Small world (rewiring parameter k,p = 4, 0.5, each agent originally connected to 4 nearest neighbours in ring
    topology, 50% of each edge being rewired to an unconnected agent)
    12C_0   1748703
    12C_1   1748987
    12C_6   1748990
    12C_7   1748991


"""

if __name__ == '__main__':

    jobIDsB = ['1748699', '1749037', '1749038', '1749039']
    jobIDsC = ['1748703', '1748987', '1748990', '1748991']

    strategyIDs = [0, 1, 6, 7]

    newXLabels = list(range(0, 21, 2))
    newXTicks = np.arange(0, 1, 0.1)
    newXTicks = [round(x, 3) for x in newXTicks]

    ## 12A ##

    ## 12B ##

    # Proportion of Cooperation
    plotAllStrategiesForVariableCooperation(jobIDsB, strategyIDs, [])
    plt.title(f'LrGePL vs Initial Proportion of Mutants')
    plt.xlabel("Initial Proportion of Mutants")
    plt.ylabel("Average Final Proportion of Cooperation")
    plt.legend(loc='lower left')
    plt.xticks(newXLabels, newXTicks)
    plt.savefig("12B_initialState_scale-free_cooperation")
    # plt.show()

    # Proportion of Strategies
    plotAllStrategyProportions(jobIDsB, strategyIDs)
    plt.title(f'LrGePL vs Initial Proportion of Mutants')
    plt.xlabel("Initial Proportion of Mutants")
    plt.ylabel("Average Final Proportion of Strategies")
    plt.legend(loc='lower left')
    plt.xticks(newXLabels, newXTicks)
    plt.savefig("12B_initialState_scale-free_proportion")
    # plt.show()

    ## 12C ##

    # Proportion of Cooperation
    plotAllStrategiesForVariableCooperation(jobIDsC, strategyIDs, [])
    plt.title(f'LrGeWSSW vs Initial Proportion of Mutants')
    plt.xlabel("Initial Proportion of Mutants")
    plt.ylabel("Average Final Proportion of Cooperation")
    plt.legend(loc='lower left')
    plt.xticks(newXLabels, newXTicks)
    plt.savefig("12C_initialState_small-world_cooperation")
    # plt.show()

    # Proportion of Strategies
    plotAllStrategyProportions(jobIDsC, strategyIDs)
    plt.title(f'LrGeWSSW vs Initial Proportion of Mutants')
    plt.xlabel("Initial Proportion of Mutants")
    plt.ylabel("Average Final Proportion of Strategies")
    plt.legend(loc='lower left')
    plt.xticks(newXLabels, newXTicks)
    plt.savefig("12C_initialState_small-world_proportion")
    # plt.show()