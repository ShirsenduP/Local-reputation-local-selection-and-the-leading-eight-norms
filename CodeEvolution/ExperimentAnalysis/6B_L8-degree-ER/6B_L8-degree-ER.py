"""
Experiment 6B

Effect of degree on regular random lattice on proportions of cooperation
Strategy i = [0,1,6,7] vs degree d = [3, 10, 25, 50, 100, 200, 299], LrGe, ONLY TEN REPEATS

    6B_0    1631629  (1631630)  NOTE: all .csv files found in first jobID folder
    6B_1    1631631  (1631632)
    6B_6    1631633  (1631634)
    6B_7    1631635  (1631636)


Effect of equivalent density on Erdos Renyi random network, LrGe

    6C_0    1759821  (1737593)  NOTE: all .csv files found in first jobID folder
    6C_1    1759822  (1737195)
    6C_6    1759823  (1737199)
    6C_7    1759824  (1737203)

"""
from CodeEvolution import Config
from CodeEvolution.ExperimentAnalysis.analysis import *
from CodeEvolution.structures import RandomRegularLattice as RRL

if __name__ == '__main__':
    jobIDsB = ['1631629', '1631631', '1631633', '1631635']
    jobIDsC = ['1759821', '1759822', '1759823', '1759824']

    degrees = [10, 100, 200, 299]
    strategyIDs = [0, 1, 6, 7]
    equivalent_densities = []
    for d in degrees:
        config = Config(size=300, degree=d)
        equivalent_densities.append(round(RRL.getTheoreticalDensity(config),3))

    fig, axes = plt.subplots(2, 2, sharex='col', sharey='all')
    plt.subplots_adjust(left=0.05, right=0.6, bottom=0.15, top=0.6)
    # 6B RRL DEGREE TEST
    for ID, strategyID in zip(jobIDsB, strategyIDs):

        data = getDataFromID(ID)
        length = data[0].shape[0]
        means = [round(table[f'Prop. Strategy #{strategyID}'].mean(), 5) for _, table in data.items()]
        stds = [round(table[f'Prop. Strategy #{strategyID}'].std() / np.sqrt(length), 5) for _, table in data.items()]
        up = [mean + std for mean, std in zip(means, stds)]
        down = [mean - std for mean, std in zip(means, stds)]
        axes[0][0].plot(degrees, means, label=f'$s_{strategyID}$', marker='.')
        axes[0][0].fill_between(degrees, down, up, alpha=0.1, antialiased=True)
    # plt.xticks(degrees, [], rotation=90)

    for ID, strategyID in zip(jobIDsB, strategyIDs):

        data = getDataFromID(ID)
        length = data[0].shape[0]
        means = [round(table['Prop. of Cooperators'].mean(), 5) for _, table in data.items()]
        stds = [round(table['Prop. of Cooperators'].std() / np.sqrt(length), 5) for _, table in data.items()]
        up = [mean + std for mean, std in zip(means, stds)]
        down = [mean - std for mean, std in zip(means, stds)]
        axes[1][0].plot(degrees, means, label=f'$s_{strategyID}$', marker='.')
        axes[1][0].fill_between(degrees, down, up, alpha=0.1, antialiased=True)
    # plt.xticks(degrees, degrees, rotation=90)
    # 6C ER DENSITY COMPARISON TEST

    for ID, strategyID in zip(jobIDsC, strategyIDs):

        data = getDataFromID(ID)
        length = data[0].shape[0]
        means = [round(table[f'Prop. Strategy #{strategyID}'].mean(), 5) for _, table in data.items()]
        stds = [round(table[f'Prop. Strategy #{strategyID}'].std() / np.sqrt(length), 5) for _, table in data.items()]
        up = [mean + std for mean, std in zip(means, stds)]
        down = [mean - std for mean, std in zip(means, stds)]
        axes[0][1].plot(degrees, means, label=f'$s_{strategyID}$', marker='.')
        axes[0][1].fill_between(degrees, down, up, alpha=0.1, antialiased=True)
    # plt.xticks(degrees, [], rotation=90)

    for ID, strategyID in zip(jobIDsC, strategyIDs):

        data = getDataFromID(ID)
        length = data[0].shape[0]
        means = [round(table['Prop. of Cooperators'].mean(), 5) for _, table in data.items()]
        stds = [round(table['Prop. of Cooperators'].std() / np.sqrt(length), 5) for _, table in data.items()]
        up = [mean + std for mean, std in zip(means, stds)]
        down = [mean - std for mean, std in zip(means, stds)]
        axes[1, 1].plot(degrees, means, label=f'$s_{strategyID}$', marker='.')
        axes[1, 1].fill_between(degrees, down, up, alpha=0.1, antialiased=True)

    # fig.suptitle("Effect of Heterogeneity", fontsize=16, y=1)
    labels = [f'$s_{strategyID}$' for strategyID in strategyIDs]
    plt.figlegend(labels=labels,
                  loc='lower center',
                  framealpha=1,
                  bbox_to_anchor=(0.55, 0.1),
                  ncol=4,
                  fancybox=True)
    plt.xticks(degrees, equivalent_densities)

    axes[1,0].set_ylabel("Prop. of \nCooperators")
    axes[0,0].set_ylabel("Prop. of \nStrategy")
    axes[0,0].set_title("$d$-RRL")
    axes[0,1].set_title("ER")

    plt.show()
    # plt.savefig('6B_heterogeneity', dpi=fig.dpi) # DPI SCALE WEIRD
