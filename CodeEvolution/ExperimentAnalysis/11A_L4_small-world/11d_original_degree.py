from CodeEvolution.ExperimentAnalysis.analysis import *

"""
Experiment 11D-----------------------------------------------------------------------

    WSSW networks changing the original value of k prior to rewiring. Setting rewiring to 0.001 (from small world paper)

    11D_0   1803837
    11D_1   1803838
    11D_2   1803839
    11D_3   1803840
    11D_4   1803841
    11D_5   1803842
    11D_6   1803843
    11D_7   1803844

    
"""


if __name__ == '__main__':

    jobIDs = ['1803837', '1803838', '1803839', '1803840', '1803841', '1803842', '1803843', '1803844']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = [0, 1, 6, 7]
    # skip = []

    xlabels = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    # xticks = list()

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all')
    # labels = [f'$s_{strategyID}$' for strategyID in strategyIDs if strategyID not in skip]

    plt.sca(ax1)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip, var=xlabels)
    # ax1.set_xticks(xticks)
    # ax1.set_xticklabels(xlabels)
    ax1.set_ylabel("Prop. of \nStrategy")
    # ax1.set_xscale('log')

    plt.sca(ax2)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip, var=xlabels)
    # ax2.set_xticks(xticks)
    # ax2.set_xticklabels(xlabels)
    ax2.set_xlabel('$k$')
    ax2.set_ylabel("Prop. of \nCooperators")
    # ax2.set_xscale('log')


    handles, labels = ax2.get_legend_handles_labels()
    lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    plt.savefig('11D_original_degree', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()