"""
Experiment 10A

Effect of increasing the mutation rate on LrGeERNetwork to see where the threshold is for mutation to dominate
Range from 0.1, 0.5 - 10 in 0.5 increments. Recall this parameter represents the expected number of mutations/time-step.

    10A_0   1574518
    10A_1   1574519
    10A_6   1574520
    10A_7   1574521

"""

from CodeEvolution.ExperimentAnalysis.analysis import *

if __name__ == '__main__':
    jobIDs = ['1574518', '1574519', '1574520', '1574521']

    # Data was generated in reverse order, fix by using reverse labels
    newXTicks = [0.1] + list(range(1, 11))
    newXLabels = [0.1] + list(np.arange(0.5, 10.1, 0.5))
    strats = [0, 1, 6, 7]

    # Plots of cooperation
    for i, ID in zip(strats, jobIDs):
        data = getDataFromID(ID)
        fig, ax = plotCooperationProportion(data)
        title = f'LrGe - $S_{i}$ vs Mutation Rate'
        plt.title(title)
        plt.xlabel("Rate of Mutation")
        plt.ylabel(f"Average Proportion of Cooperation")
        plt.xticks(ticks=newXTicks, labels=newXLabels)
        plt.savefig(ID+'_cooperation')
        # plt.show()

    # Plots of proportions of strategies
    for i, ID in zip(strats, jobIDs):
        data = getDataFromID(ID)
        fig, ax = plotSingleStrategy(data, i)
        title = f'LrGe - $S_{i}$ vs Mutation Rate'
        plt.title(title)
        plt.xlabel("Rate of Mutation")
        plt.ylabel(f"Average Final Proportion")
        plt.xticks(ticks=newXTicks, labels=newXLabels)
        plt.savefig(ID+'_proportion')
        # plt.show()