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
    xticks, xlabels = list(range(9)), list(range(2, 11))

    plotAllStrategyCooperations(jobIDs, strategyIDs, skip)
    plt.title(f'LrGePL vs Preferential Attachment Parameter')
    plt.xlabel("$m$")
    plt.ylabel(f"Average Final Proportion of Cooperation")
    plt.xticks(xticks, xlabels)
    plt.legend(loc='lower right')
    plt.savefig("8A_preferential-attachment")
    # plt.show()
