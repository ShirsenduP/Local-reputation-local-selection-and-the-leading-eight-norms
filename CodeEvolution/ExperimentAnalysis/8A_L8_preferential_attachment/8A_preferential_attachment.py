from CodeEvolution.ExperimentAnalysis.analysis import *

"""
Experiment 8A-----------------------------------------------------------------------

Effect of the preferential attachment parameter on l8 on scale-free network

m = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    8A.0    1536580
    8A.1    1536581
    8A.6    1536582
    8A.7    1536583
    
"""

if __name__ == '__main__':

    jobIDs = ['1536580', '1536581', '1536582', '1536583']
    strategyIDs = [0, 1, 6, 7]

    for strategy, jobID in zip(strategyIDs, jobIDs):
        data = getDataFromID(jobID)
        fig, ax = plotCooperationProportion(data)
        plt.title(f'LrGePL $s_{strategy}$ vs Preferential Attachment Parameter')
        plt.xlabel("$m$")
        plt.ylabel(f"Average Final Proportion of Cooperation")
        plt.savefig(jobID + "_cooperation")
        # plt.show()
    #
    # jobID = '1536580'
    # data = getDataFromID(jobID)
    #
    # fig, ax = plotCooperationProportion(data)
    # plt.title('LrGePL $s_0$ vs Preferential Attachment Parameter')
    # plt.xlabel("$m$")
    # plt.ylabel(f"Average Final Proportion of Cooperation")
    # plt.show()
    #
    #
    # jobID = '1536581'
    # data = getDataFromID(jobID)
    #
    # fig, ax = plotCooperationProportion(data)
    # plt.title('LrGePL $s_1$ vs Preferential Attachment Parameter')
    # plt.xlabel("$m$")
    # plt.ylabel(f"Average Final Proportion of Cooperation")
    # plt.show()
    #
    #
    # jobID = '1536582'
    # data = getDataFromID(jobID)
    #
    # fig, ax = plotCooperationProportion(data)
    # plt.title('LrGePL $s_6$ vs Preferential Attachment Parameter')
    # plt.xlabel("$m$")
    # plt.ylabel(f"Average Final Proportion of Cooperation")
    # plt.show()
    #
    #
    # jobID = '1536583'
    # data = getDataFromID(jobID)
    #
    # fig, ax = plotCooperationProportion(data)
    # plt.title('LrGePL $s_7$ vs Preferential Attachment Parameter')
    # plt.xlabel("$m$")
    # plt.ylabel(f"Average Final Proportion of Cooperation")
    # plt.show()
    #
