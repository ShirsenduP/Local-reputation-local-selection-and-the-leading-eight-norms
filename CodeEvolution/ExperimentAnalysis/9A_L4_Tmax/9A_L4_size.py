from CodeEvolution.ExperimentAnalysis.analysis import *

"""
Experiment 9A-----------------------------------------------------------------------

Effect of simulation on variance of convergence point, Erdos Renyi network, size 300, test maxT from 500-5000 at
intervals of 250 to see if maxT of 5000 is necessary for every simulation.

    9A_0    1582527
    9A_1    1576515
    9B_2    1633286
    9B_3    1633287
    9B_4    1633288
    9B_5    1633289
    9A_6    1574515
    9A_7    1574516

"""

if __name__ == '__main__':
    jobIDs = ['1582527', '1576515', '1633286', '1633287', '1633288', '1633289', '1574515', '1574516']
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    skip = [2, 3, 4, 5]
    # skip = []

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all')
    labels = [f'$s_{strategyID}$' for strategyID in strategyIDs if strategyID not in skip]
    xticks, xlabels = range(0, 20, 2), list(range(500, 5001, 500))

    plt.sca(ax1)
    plotAllStrategyProportions(jobIDs, strategyIDs, skip)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(xlabels)
    ax1.set_ylabel("Prop. of \nStrategy")

    plt.sca(ax2)
    plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip)
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xlabels)
    ax2.set_xlabel('$T_{max}$ Length of simulation')
    ax2.set_ylabel("Prop. of \nCooperators")

    handles, labels = ax2.get_legend_handles_labels()
    lgd = ax2.legend(handles, labels, loc='center right', bbox_to_anchor=(1.18, 1.1))
    plt.savefig('9A_Tmax', bbox_extra_artists=(lgd,), bbox_inches='tight')
