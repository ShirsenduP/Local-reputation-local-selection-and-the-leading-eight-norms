"""
Experiment 10D

    Exp 10A on RRL network

    E_10D0  1798041
    E_10D1  1798042
    E_10D2  1798043
    E_10D3  1798044
    E_10D4  1798045
    E_10D5  1798047
    E_10D6  1798048
    E_10D7  1798049


"""

from CodeEvolution.ExperimentAnalysis.analysis import *

if __name__ == '__main__':
############################## D

    jobIDs = ['1802831','1802832','1802833','1802834']

    strategyIDs = [0, 1, 6, 7]
    skip = [2, 3, 4, 5]

    xlabels = list(np.arange(0, 20, 2))
    xticks = list(range(0, len(xlabels)))

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all', sharey='all')


    # Proportion of Cooperation
    plt.sca(ax1)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    ax1.set_ylabel("Prop. of \nStrategy")
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabels)

    # Proportion of Strategies
    plt.sca(ax2)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax2.set_xlabel("Mutations / period")
    ax2.set_ylabel("Prop. of \nCooperators")
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xlabels)


    handles, labels = ax2.get_legend_handles_labels()
    lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18,1.1))
    plt.savefig('10C_mutation_rate_plus', bbox_extra_artists=(lgd,), bbox_inches='tight')
