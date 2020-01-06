from CodeEvolution.ExperimentAnalysis.analysis import *

"""
Experiment 8A-----------------------------------------------------------------------

Effect of the preferential attachment parameter on l8 on scale-free network

m = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    8A.0    1536580
    8A.1    1536581
    8A.2    1635795
    8A.3    1635796
    8A.4    1635797
    8A.5    1635798
    8A.6    1536582
    8A.7    1536583
    
"""

if __name__ == '__main__':
    # Leading Four
    jobIDs = ['1536580', '1536581', '1635795', '1635796', '1635797', '1635798', '1536582', '1536583']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = []
    xticks, xlabels = list(range(0, 9, 2)), list(range(2, 11, 2))
    #
    # fig, axes = plt.subplots(1, 2, sharey='all', figsize=(9, 3), dpi=80)
    # fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
    # plt.sca(axes[0])
    # plotAllStrategyCooperations(jobIDs, strategyIDs, skip)
    # axes[0].set_title('Cooperation')
    # plt.xticks(xticks, xlabels)
    # plt.ylabel('Proportion')
    #
    #
    # plt.sca(axes[1])
    # plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    # axes[1].set_title('Strategy')
    # plt.xticks(xticks, xlabels)
    #
    # labels = [f'$s_{strategyID}$' for strategyID in strategyIDs if strategyID not in skip]
    # plt.gca().legend(loc='center left', bbox_to_anchor=(1,0.5))
    # fig.text(0.5, 0.001, 'Preferential Attachment Parameter $m$', ha='center')
    # # plt.savefig("8A_Preferential-attachment")
    # plt.show()


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
    ax2.set_xlabel('Preferential Attachment Parameter')
    ax2.set_ylabel("Prop. of \nCooperators")

    handles, labels = ax2.get_legend_handles_labels()
    lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    plt.savefig('8A_preferential-attachment', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()