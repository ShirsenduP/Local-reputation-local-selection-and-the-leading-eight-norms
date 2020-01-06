"""
Experiment 10A

Effect of increasing the mutation rate on LrGeERNetwork to see where the threshold is for mutation to dominate
Range from 0.1, 0.5 - 10 in 0.5 increments. Recall this parameter represents the expected number of mutations/time-step.

    10A_0   1574518
    10A_1   1574519
    10B_2   1632729
    10B_3   1632730
    10B_4   1632731
    10B_5   1632732
    10A_6   1574520
    10A_7   1574521

"""

from CodeEvolution.ExperimentAnalysis.analysis import *

if __name__ == '__main__':
    #
    # jobIDs = ['1574518', '1574519', '1632729', '1632730', '1632731', '1632732', '1574520', '1574521']
    # strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    # skip = [2, 3, 4, 5]
    #
    # newXTicks = list(range(0, 11))
    # newXLabels = list(np.arange(0, 11, 1))
    #
    # fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all', sharey='all')
    #
    #
    # # Proportion of Cooperation
    # plt.sca(ax1)
    # plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    # ax1.set_ylabel("Prop. of \nStrategy")
    #
    # # Proportion of Strategies
    # plt.sca(ax2)
    # plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    # ax2.set_xlabel("Mutations / period")
    # ax2.set_ylabel("Prop. of \nCooperators")
    #
    # handles, labels = ax2.get_legend_handles_labels()
    # lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18,1.1))
    # plt.savefig('10A_mutation_rate', bbox_extra_artists=(lgd,), bbox_inches='tight')
    #
    # ############################# E
    #
    # jobIDs = ['1798041','1798042','1798043','1798044','1798045','1798047','1798048','1798049']
    # strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    # skip = [2, 3, 4, 5]
    # # skip = []
    #
    # newXTicks = list(range(0, 11))
    # newXLabels = list(np.arange(0, 11, 1))
    #
    # fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all', sharey='all')
    #
    #
    # # Proportion of Cooperation
    # plt.sca(ax1)
    # plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    # ax1.set_ylabel("Prop. of \nStrategy")
    #
    # # Proportion of Strategies
    # plt.sca(ax2)
    # plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    # ax2.set_xlabel("Mutations / period")
    # ax2.set_ylabel("Prop. of \nCooperators")
    #
    # handles, labels = ax2.get_legend_handles_labels()
    # lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18,1.1))
    # plt.savefig('10D_mutation_rate_rrl', bbox_extra_artists=(lgd,), bbox_inches='tight')
    #
    # ############################# E
    #
    # """
    # Experiment 10E
    #
    #     Exp 10A on Scale free network
    #
    #     E_10E0  1798050
    #     E_10E1  1798051
    #     E_10E2  1798052
    #     E_10E3  1798053
    #     E_10E4  1798054
    #     E_10E5  1798055
    #     E_10E6  1798056
    #     E_10E7  1798057
    #
    # """
    #
    # jobIDs = ['1798050', '1798051', '1798052', '1798053', '1798054', '1798055', '1798056', '1798057']
    #
    # strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    # skip = [2, 3, 4, 5]
    # # skip = []
    #
    # newXTicks = list(range(0, 11))
    # newXLabels = list(np.arange(0, 20, 2))
    #
    # fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all', sharey='all')
    #
    # # Proportion of Cooperation
    # plt.sca(ax1)
    # plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    # ax1.set_ylabel("Prop. of \nStrategy")
    #
    # # Proportion of Strategies
    # plt.sca(ax2)
    # plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    # ax2.set_xlabel("Mutations / period")
    # ax2.set_ylabel("Prop. of \nCooperators")
    #
    # handles, labels = ax2.get_legend_handles_labels()
    # lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    # plt.savefig('10E_mutation_rate_pl', bbox_extra_artists=(lgd,), bbox_inches='tight')
    #
    # ############################## E
    # """
    # Experiment 10E
    #
    #     Exp 10A on WSSW network
    #
    #     E_10F0  1798058
    #     E_10F1  1798059
    #     E_10F2  1798060
    #     E_10F3  1798061
    #     E_10F4  1798062
    #     E_10F5  1798063
    #     E_10F6  1798064
    #     E_10F7  1798065
    #
    # """
    #
    # jobIDs = ['1798058','1798059','1798060','1798061','1798062','1798063','1798064','1798065']
    #
    # strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    # skip = [2, 3, 4, 5]
    # # skip = []
    #
    # newXTicks = list(range(0, 11))
    # newXLabels = list(np.arange(0, 20, 2))
    #
    # fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all', sharey='all')
    #
    # # Proportion of Cooperation
    # plt.sca(ax1)
    # plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    # ax1.set_ylabel("Prop. of \nStrategy")
    #
    # # Proportion of Strategies
    # plt.sca(ax2)
    # plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    # ax2.set_xlabel("Mutations / period")
    # ax2.set_ylabel("Prop. of \nCooperators")
    #
    # handles, labels = ax2.get_legend_handles_labels()
    # lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    # plt.savefig('10F_mutation_rate_wssw', bbox_extra_artists=(lgd,), bbox_inches='tight')
    #
    # ############################## C
    #
    #
    #

    fig, ax = plt.subplots(4, 2, sharex='all', sharey='all')
    # fig.tight_layout()
    ax1 = ax[0, 0]
    ax2 = ax[0, 1]
    ax3 = ax[1, 0]
    ax4 = ax[1, 1]
    ax5 = ax[2, 0]
    ax6 = ax[2, 1]
    ax7 = ax[3, 0]
    ax8 = ax[3, 1]

    ###############################################################################################
    # ER
    jobIDs = ['1574518', '1574519', '1632729', '1632730', '1632731', '1632732', '1574520', '1574521']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = []
    xticks, xlabels = range(0, 11, 2), list(range(0, 11, 2))
    # newXTicks = list(range(0, 11))
    # newXLabels = list(np.arange(0, 11, 1))
    plt.sca(ax1)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabels)

    plt.sca(ax2)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xlabels)
    ax2.text(11.5, 0.5, "ER", size='9')
    # ax2.set_xlabel('Size of Network $n$')
    # ax2.set_ylabel("Prop. of \nCooperators")

    handles, labels = ax2.get_legend_handles_labels()
    # lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    # plt.savefig('8B_size', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()

    ###############################################################################################
    # RRL
    jobIDs = ['1798041','1798042','1798043','1798044','1798045','1798047','1798048','1798049']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = []

    # fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all')
    # xticks, xlabels = range(0, 10, 1), list(range(50, 550, 50))
    # labels = [f'$s_{strategyID}$' for strategyID in strategyIDs if strategyID not in skip]

    plt.sca(ax3)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    ax3.set_xticks(xticks)
    ax3.set_xticklabels(xlabels)

    plt.sca(ax4)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax4.set_xticks(xticks)
    ax4.set_xticklabels(xlabels)
    ax4.text(11.5, 0.5, "4-RRL", size='9')
    # ax4.set_xlabel('Size of Network $n$')
    # ax4.set_ylabel("Prop. of \nCooperators")

    # handles, labels = ax2.get_legend_handles_labels()
    # lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    # plt.savefig('8C_size_rrl', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()
    ###############################################################################################
    # SF/PL
    jobIDs = ['1798050', '1798051', '1798052', '1798053', '1798054', '1798055', '1798056', '1798057']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = []

    # fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all')
    # xticks, xlabels = range(0, 10, 1), list(range(50, 550, 50))
    # labels = [f'$s_{strategyID}$' for strategyID in strategyIDs if strategyID not in skip]

    plt.sca(ax5)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    ax5.set_xticks(xticks)
    ax5.set_xticklabels(xlabels)

    plt.sca(ax6)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax6.set_xticks(xticks)
    ax6.set_xticklabels(xlabels)
    ax6.text(11.5, 0.5, "SF", size='9')
    # ax6.set_xlabel('Size of Network $n$')
    # ax6.set_ylabel("Prop. of \nCooperators")

    # handles, labels = ax6.get_legend_handles_labels()
    # lgd = ax4.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    # plt.savefig('8D_size_pl', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()
    ###############################################################################################
    # WSSW
    # jobIDs = ['1798058','1798059','1798060','1798061','1798062','1798063','1798064','1798065']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = []

    # fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all')
    # xticks, xlabels = range(0, 10, 1), list(range(50, 550, 50))
    # labels = [f'$s_{strategyID}$' for strategyID in strategyIDs if strategyID not in skip]

    plt.sca(ax7)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    ax7.set_xticks(xticks)
    ax7.set_xticklabels(xlabels)

    plt.sca(ax8)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax8.set_xticks(xticks)
    ax8.set_xticklabels(xlabels)
    ax8.text(11.5, 0.5, "SW", size='9')
    # ax8.set_xlabel('Size of Network $n$')
    # ax8.set_ylabel("Prop. of \nCooperators")

    # Text labels
    fig.text(0.5, 0.03, 'Mutations / period', ha='center', va='center')
    fig.text(0.07, 0.5, 'Prop. of Strategy', ha='center', va='center', rotation='vertical')
    fig.text(0.52, 0.5, 'Prop. of Cooperation', ha='center', va='center', rotation='vertical')

    # Network labels
    # fig.text(0.075, 0.2, 'SW', ha='center', va='center')

    handles, labels = ax2.get_legend_handles_labels()
    lgd = ax2.legend(handles, labels, loc='upper center', bbox_to_anchor=(-0.04, 1.6), ncol=4)
    plt.savefig('10_mutation_combined', bbox_extra_artists=(lgd,))
    # plt.show()

