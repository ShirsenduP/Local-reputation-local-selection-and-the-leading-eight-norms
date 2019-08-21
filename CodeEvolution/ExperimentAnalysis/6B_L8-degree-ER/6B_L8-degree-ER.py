"""
Experiment 6B

Effect of degree of regular random lattice on proportions of cooperation
Strategy i = [0,7] vs degree d [13, 3]

    6A_0
    6A_1
    6A_6
    6A_7

"""

from CodeEvolution.ExperimentAnalysis.analysis import *

if __name__ == '__main__':
    jobIDs = ['1557510', '1557511', '1536574', '1536575', '1536576', '1536577', '1557512', '1560446']

    # Data was generated in reverse order, fix by using reverse labels
    newXLabels = list(range(13, 2, -1))
    i = 0

    # Plots of cooperation
    for ID in jobIDs:
        data = getDataFromID(ID)
        if i in [2, 3, 4, 5]:
            i += 1
            continue
        fig, ax = plotCooperationProportion(data)
        title = f'LrGe - $S_{i}$ vs RRL Degree'
        plt.title(title)
        plt.xlabel("Degree")
        plt.ylabel(f"Average Proportion of Cooperation")
        plt.xticks(ticks=list(range(11)), labels=newXLabels)
        plt.savefig(+ID)
        # plt.show()
        i += 1
