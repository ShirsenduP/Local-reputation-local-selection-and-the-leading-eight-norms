from CodeEvolution.ExperimentAnalysis.analysis import *

"""
Experiment 8C - COMPLETED (COMBINED PLOT)

Effect of increasing size on LrGe ER network
	8B.0    1746310
	8B.1    1746316
	8B.2    1746320
	8B.3    1746323
	8B.4    1748536
	8B.5    1748537
	8B.6    1748538
	8B.7    1748539

Effect of increasing size on LrGe RRL network with d=4

	8C_0    1797984
	8C_1    1797985
	8C_2    1797986
	8C_3    1797987
	8C_4    1797988
	8C_5    1797989
	8C_6    1797990
	8C_7    1797991

Experiment 8D - IN PROGRESS

Effect of increasing size on LrGe PL network with pref attachment = 2

	8D_0    1797992
	8D_1    1797993
	8D_2    1797994
	8D_3    1797995
	8D_4    1797996
	8D_5    1797997
	8D_6    1797998
	8D_7    1797999

Experiment 8E - IN PROGRESS

Effect of increasing size on LrGe WSSW network with (4, 0.001)

	8E_0    1798002
	8E_1    1798003
	8E_2    1798004
	8E_3    1798005
	8E_4    1798006
	8E_5    1798007
	8E_6    1798008
	8E_7    1798009


"""

if __name__ == '__main__':
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
    jobIDs = ['1746310', '1746316', '1746320', '1746323', '1748536', '1748537', '1748538', '1748539']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = []
    xticks, xlabels = range(0, 10, 2), list(range(50, 550, 100))

    plt.sca(ax1)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabels)

    plt.sca(ax2)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xlabels)
    ax2.text(10.3, 0.5, "ER", size='9')
    # ax2.set_xlabel('Size of Network $n$')
    # ax2.set_ylabel("Prop. of \nCooperators")

    handles, labels = ax2.get_legend_handles_labels()
    # lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    # plt.savefig('8B_size', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()



    ###############################################################################################
    # RRL
    jobIDs = ['1797984', '1797985', '1797986', '1797987', '1797988', '1797989', '1797990', '1797991']
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
    ax4.text(10.3, 0.5, "4-RRL", size='9')
    # ax4.set_xlabel('Size of Network $n$')
    # ax4.set_ylabel("Prop. of \nCooperators")

    # handles, labels = ax2.get_legend_handles_labels()
    # lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    # plt.savefig('8C_size_rrl', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()
    ###############################################################################################
    # SF/PL
    jobIDs = ['1797992', '1797993', '1797994', '1797995', '1797996', '1797997', '1797998', '1797999']
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
    ax6.text(10.3, 0.5, "SF", size='9')
    # ax6.set_xlabel('Size of Network $n$')
    # ax6.set_ylabel("Prop. of \nCooperators")

    # handles, labels = ax6.get_legend_handles_labels()
    # lgd = ax4.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    # plt.savefig('8D_size_pl', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()
    ###############################################################################################
    # WSSW
    jobIDs = ['1798002', '1798003', '1798004', '1798005', '1798006', '1798007', '1798008', '1798009']
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
    ax8.text(10.3, 0.5, "SW", size='9')
    # ax8.set_xlabel('Size of Network $n$')
    # ax8.set_ylabel("Prop. of \nCooperators")

    # Text labels
    fig.text(0.5, 0.03, 'Size of Network $N$', ha='center', va='center')
    fig.text(0.07, 0.5, 'Prop. of Strategy', ha='center', va='center', rotation='vertical')
    fig.text(0.52, 0.5, 'Prop. of Cooperation', ha='center', va='center', rotation='vertical')

    # Network labels
    # fig.text(0.075, 0.2, 'SW', ha='center', va='center')


    handles, labels = ax2.get_legend_handles_labels()
    lgd = ax2.legend(handles, labels, loc='upper center', bbox_to_anchor=(-0.04, 1.6), ncol=4)
    plt.savefig('8DCE_size_combined', bbox_extra_artists=(lgd,))
    # plt.show()
