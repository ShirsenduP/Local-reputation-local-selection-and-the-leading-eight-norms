from CodeEvolution.ExperimentAnalysis.analysis import *

"""
Experiment 11A-----------------------------------------------------------------------


    Redo 11A/11B for more appropriate range of values of rewiring probability on logscale from 10^-3 to 10^0

    11C_0   1780485
    11C_1   1780487
    11C_2   1770601
    11C_3   1770602
    11C_4   1770603
    11C_5   1770604
    11C_6   1780488
    11C_7   1780489
    
"""

if __name__ == '__main__':

    jobIDs = ['1780485', '1780487', '1770601', '1770602', '1770603', '1770604', '1780488', '1780489']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = []

    xlabels = np.logspace(-4, 0, 40)
    xticks = list(range(len(xlabels)))

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all')
    # labels = [f'$s_{strategyID}$' for strategyID in strategyIDs if strategyID not in skip]

    plt.sca(ax1)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip, var=xlabels)
    # ax1.set_xticks(xticks)
    # ax1.set_xticklabels(xlabels)
    ax1.set_ylabel("Prop. of \nStrategy")
    ax1.set_xscale('log')
    plt.sca(ax2)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip, var=xlabels)
    # ax2.set_xticks(xticks)
    # ax2.set_xticklabels(xlabels)
    ax2.set_xlabel('Rewiring Probability')
    ax2.set_ylabel("Prop. of \nCooperators")
    ax2.set_xscale('log')


    handles, labels = ax2.get_legend_handles_labels()
    lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    plt.savefig('11C_rewiring-probability', bbox_extra_artists=(lgd,), bbox_inches='tight')
