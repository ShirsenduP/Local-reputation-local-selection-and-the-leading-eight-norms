from CodeEvolution.ExperimentAnalysis.analysis import *

"""
Experiment 12ABC-----------------------------------------------------------------------

    Allowing no mutation, but modulating the initial proportion of mutants in the population to find the limiting point
    of where the network can recover. Range 0-1 in 0.05 increments.

Experiment 12A - INCOMPLETE
    Erdos Renyi (Tmax 2500, rep 25)
    12A_0   1804227   (1804227)
    12A_1   1804228   (1804228)
    12A_2   1804229   
    12A_3   1804230   
    12A_4   1804231   
    12A_5   1804232   
    12A_6   1804233   (1804229)
    12A_7   1804234   (1804230)
    
1804227 2.04621 E_12A0     ucabpod      qw    09/15/2019 15:11:37                                    1        
1804228 2.04390 E_12A1     ucabpod      qw    09/15/2019 15:11:38                                    1        
1804229 2.04181 E_12A2     ucabpod      qw    09/15/2019 15:11:40                                    1        
1804230 2.03991 E_12A3     ucabpod      qw    09/15/2019 15:11:42                                    1        
1804231 0.00000 E_12A4     ucabpod      qw    09/15/2019 15:11:43                                    1        
1804232 0.00000 E_12A5     ucabpod      qw    09/15/2019 15:11:44                                    1        
1804233 0.00000 E_12A6     ucabpod      qw    09/15/2019 15:11:46                                    1        
1804234 0.00000 E_12A7     ucabpod      qw    09/15/2019 15:11:47                                    1                               1     

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
    
Experiment 12D - IN PROGRESS

RRL d=4
    12D_0   1804177
    12D_1   1804178
    12D_2   1804179
    12D_3   1804180
    12D_4   1804181
    12D_5   1804182
    12D_6   1804183
    12D_7   1804184
    
                           1        


"""

if __name__ == '__main__':
    fig, ax = plt.subplots(4, 2, sharex='col', sharey='all')
    # fig, ax = plt.subplots(4, 2)
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
    # jobIDs = ['1574518', '1574519', '1632729', '1632730', '1632731', '1632732', '1574520', '1574521']
    jobIDs = []
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = []
    xticks = list(range(2, 23, 2))
    xlabels = np.arange(0.1, 1.11, 0.1)
    xlabels = [round(x, 3) for x in xlabels]

    plt.sca(ax1)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabels)
    ax1.set_xlim(15, 20)

    plt.sca(ax2)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xlabels)
    ax2.text(20.5, 0.92, "ER", size='9')
    ax2.set_xlim(15, 20)
    # ax2.set_xlabel('Size of Network $n$')
    # ax2.set_ylabel("Prop. of \nCooperators")

    handles, labels = ax2.get_legend_handles_labels()
    # lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    # plt.savefig('8B_size', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()

    ###############################################################################################
    # RRL
    # jobIDs = ['1798041', '1798042', '1798043', '1798044', '1798045', '1798047', '1798048', '1798049']
    jobIDs = []
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
    ax3.set_xlim(15, 20)

    plt.sca(ax4)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax4.set_xticks(xticks)
    ax4.set_xticklabels(xlabels)
    ax4.text(20.5, 0.92, "4-RRL", size='9')
    ax4.set_xlim(15, 20)
    # ax4.set_xlabel('Size of Network $n$')
    # ax4.set_ylabel("Prop. of \nCooperators")

    # handles, labels = ax2.get_legend_handles_labels()
    # lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    # plt.savefig('8C_size_rrl', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()
    ###############################################################################################
    # SF/PL
    jobIDs = ['1748699', '1749037', '1770567', '1770568', '1770569', '1770570', '1749038', '1749039']
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
    ax5.set_xlim(15, 20)

    plt.sca(ax6)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax6.set_xticks(xticks)
    ax6.set_xticklabels(xlabels)
    ax6.text(20.5, 0.92, "SF", size='9')
    ax6.set_xlim(15, 20)
    # ax6.set_xlabel('Size of Network $n$')
    # ax6.set_ylabel("Prop. of \nCooperators")

    # handles, labels = ax6.get_legend_handles_labels()
    # lgd = ax4.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    # plt.savefig('8D_size_pl', bbox_extra_artists=(lgd,), bbox_inches='tight')
    # plt.show()
    ###############################################################################################
    # WSSW
    jobIDs = ['1770559', '1770560', '1770561', '1770562', '1770563', '1770564', '1770565', '1770566']
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
    ax7.set_xlim(15, 20)

    plt.sca(ax8)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax8.set_xticks(xticks)
    ax8.set_xticklabels(xlabels)
    ax8.set_xlim(15, 20)
    # ax8.set_xlabel('Size of Network $n$')
    # ax8.set_ylabel("Prop. of \nCooperators")

    # Text labels
    fig.text(0.5, 0.03, 'Initial Proportion of All-D', ha='center', va='center')
    fig.text(0.05, 0.5, 'Prop. of Strategy', ha='center', va='center', rotation='vertical')
    fig.text(0.52, 0.5, 'Prop. of Cooperation', ha='center', va='center', rotation='vertical')
    ax8.text(20.5, 0.92, "SW", size='9')

    # Network labels
    # fig.text(0.075, 0.2, 'SW', ha='center', va='center')

    handles, labels = ax8.get_legend_handles_labels()
    lgd = ax2.legend(handles, labels, loc='upper center', bbox_to_anchor=(-0.04, 1.6), ncol=4)
    plt.savefig('12_initial_state_combined', bbox_extra_artists=(lgd,))
    # plt.show()

