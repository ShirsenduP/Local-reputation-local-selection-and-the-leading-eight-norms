"""
Experiment 6B

Effect of degree on regular random lattice on proportions of cooperation
Strategy i = [0,1,6,7] vs degree d = [3, 10, 25, 50, 100, 200, 299], LrGe, ONLY TEN REPEATS

    6B_0    1631629
    6B_1    1631631
    6B_6    1631633
    6B_7    1631635

"""

from CodeEvolution.ExperimentAnalysis.analysis import *

if __name__ == '__main__':
    jobIDs = ['1631629', '1631631', '1631633', '1631635']
    degrees = [3, 10, 25, 50, 100, 200, 299]
    strategyIDs = [0, 1, 6, 7]

    fig, ax = plt.subplots()
    for ID, strategyID in zip(jobIDs, strategyIDs):

        data = getDataFromID(ID)
        length = data[0].shape[0]
        means = [round(table[f'Prop. Strategy #{strategyID}'].mean(), 5) for _, table in data.items()]
        stds = [round(table[f'Prop. Strategy #{strategyID}'].std() / np.sqrt(length), 5) for _, table in data.items()]
        up = [mean + std for mean, std in zip(means, stds)]
        down = [mean - std for mean, std in zip(means, stds)]
        plt.plot(degrees, means, label=f'$s_{strategyID}$')
        plt.fill_between(degrees, down, up, alpha=0.1, antialiased=True)

    plt.title(f'LrGeRRL vs Number of neighbours $d$')
    plt.xlabel('Number of neighbours $d$')
    plt.ylabel('Average Final Proportion of Strategy')
    plt.xticks(degrees, degrees, rotation=90)
    plt.legend(bbox_to_anchor=(0.45, 0.35))
    plt.tight_layout()
    # plt.savefig('6B_rrl_proportion')
    plt.show()

    # fig, ax = plt.subplots()
    # for ID, strategyID in zip(jobIDs, strategyIDs):
    #
    #     data = getDataFromID(ID)
    #     length = data[0].shape[0]
    #     means = [round(table['Prop. of Cooperators'].mean(), 5) for _, table in data.items()]
    #     stds = [round(table['Prop. of Cooperators'].std() / np.sqrt(length), 5) for _, table in data.items()]
    #     up = [mean + std for mean, std in zip(means, stds)]
    #     down = [mean - std for mean, std in zip(means, stds)]
    #     plt.plot(degrees, means, label=f'$s_{strategyID}$')
    #     plt.fill_between(degrees, down, up, alpha=0.1, antialiased=True)
    #
    # plt.title(f'LrGeRRL vs Number of neighbours $d$')
    # plt.xlabel('Number of neighbours $d$')
    # plt.ylabel('Average Proportion of Cooperation')
    # plt.xticks(degrees, degrees, rotation=90)
    # plt.legend(bbox_to_anchor=(0.45, 0.35), )
    # plt.tight_layout()
    # # plt.show()
    # plt.savefig('6B_rrl_cooperation')