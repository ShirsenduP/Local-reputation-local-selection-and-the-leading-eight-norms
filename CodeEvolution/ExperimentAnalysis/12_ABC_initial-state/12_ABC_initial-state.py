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
    12B_2   1770567
    12B_3   1770568
    12B_4   1770569
    12B_5   1770570
    12B_6   1749038
    12B_7   1749039

Experiment 12C - DONE

    Small world (rewiring parameter k,p = 4, 0.5, each agent originally connected to 4 nearest neighbours in ring
    topology, 50% of each edge being rewired to an unconnected agent)
    12C_0   1748703     OLD
    12C_1   1748987     OLD
    12C_6   1748990     OLD
    12C_7   1748991     OLD
    
    Small world (rewiring parameter k,p = 4, 0.01)
    12C_0   1770559
    12C_1   1770560
    12C_2   1770561
    12C_3   1770562
    12C_4   1770563
    12C_5   1770564
    12C_6   1770565
    12C_7   1770566


"""

if __name__ == '__main__':

    jobIDsB = ['1748699', '1749037', '1770567', '1770568', '1770569', '1770570', '1749038', '1749039']
    # jobIDsC = ['1748703', '1748987', '1748990', '1748991']
    jobIDsC = ['1770559', '1770560', '1770561', '1770562', '1770563', '1770564', '1770565', '1770566']

    # strategyIDs = [0, 1, 6, 7]
    strategyIDs = list(range(8))

    newXLabels = list(range(0, 21, 10))
    newXTicks = np.arange(0, 1.01, 0.5)
    newXTicks = [round(x, 3) for x in newXTicks]

    ## 12A ##

    ## 12B ##

    # Proportion of Cooperation
    plt.subplot(2, 3, 2)
    plotAllStrategiesForVariableCooperation(jobIDsB, strategyIDs, [])
    # plt.title(f'LrGePL vs Initial Proportion of Mutants')
    plt.xlabel("Initial Proportion of Mutants")
    # plt.ylabel("Average Final Proportion of Cooperation")
    # plt.legend(loc='lower left')
    plt.xticks(newXLabels, newXTicks)
    # plt.savefig("12B_initialState_scale-free_cooperation")
    # plt.show()

    # Proportion of Strategies
    plt.subplot(2, 3, 5)
    plotAllStrategyProportions(jobIDsB, strategyIDs)
    # plt.title(f'LrGePL vs Initial Proportion of Mutants')
    plt.xlabel("Initial Proportion of Mutants")
    # plt.ylabel("Average Final Proportion of Strategies")
    # plt.legend(loc='lower left')
    plt.xticks(newXLabels, newXTicks)
    # plt.savefig("12B_initialState_scale-free_proportion")
    # plt.show()

    ## 12C ##

    # Proportion of Cooperation
    plt.subplot(2, 3, 3)
    plotAllStrategiesForVariableCooperation(jobIDsC, strategyIDs, [])
    # plt.suptitle(f'LrGeWSSW vs Initial Proportion of Mutants')
    plt.xlabel("Initial Proportion of Mutants")
    plt.ylabel("Prop. of Cooperation")
    # plt.legend(loc='center right')
    plt.xticks(newXLabels, newXTicks)
    # plt.savefig("12C_initialState_small-world_cooperation")
    # plt.show()

    # Proportion of Strategies
    plt.subplot(2, 3, 6)
    plotAllStrategyProportions(jobIDsC, strategyIDs)
    # plt.title(f'LrGeWSSW vs Initial Proportion of Mutants')
    plt.xlabel("Initial Proportion of Mutants")
    plt.ylabel("Prop. of Strategies")
    # plt.legend(loc='best', ncol=4)
    plt.xticks(newXLabels, newXTicks)
    # plt.savefig("12C_initialState_small-world_proportion")
    plt.tight_layout()
    plt.show()
