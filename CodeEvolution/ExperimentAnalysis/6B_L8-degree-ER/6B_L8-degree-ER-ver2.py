"""
Experiment 6B

Effect of degree on regular random lattice on proportions of cooperation
Strategy i = [0,1,6,7] vs degree d = [3, 10, 25, 50, 100, 200, 299], LrGe, ONLY TEN REPEATS

    6B_0    1631629  (1631630)  NOTE: all .csv files found in first jobID folder
    6B_1    1631631  (1631632)
    6B_2    1847719
    6B_3    1847720
    6B_4    1847721
    6B_5    1847722
    6B_6    1631633  (1631634)
    6B_7    1631635  (1631636)


Effect of equivalent density on Erdos Renyi random network, LrGe

    6C_0    1759821  (1737593)  NOTE: all .csv files found in first jobID folder
    6C_1    1759822  (1737195)
    6C_2    1847723
    6C_3    1847724
    6C_4    1847725
    6C_5    1847726
    6C_6    1759823  (1737199)
    6C_7    1759824  (1737203)

"""
from CodeEvolution import Config
from CodeEvolution.ExperimentAnalysis.analysis import *
from CodeEvolution.structures import RandomRegularLattice as RRL

if __name__ == '__main__':
    jobIDsB = ['1631629', '1631631', '1847719', '1847720', '1847721', '1847722', '1631633', '1631635']
    jobIDsC = ['1759821', '1759822', '1847723', '1847724', '1847725', '1847726', '1759823', '1759824']

    degrees = [10, 100, 200, 299]
    strategyIDs = [0, 1, 2, 3, 4, 5, 6, 7]
    # strategyIDs = [2, 3, 4, 5]
    equivalent_densities = []
    for d in degrees:
        config = Config(size=300, degree=d)
        equivalent_densities.append(round(RRL.getTheoreticalDensity(config), 2))

    ## PLOTS

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
        axes[0][0].fill_between(degrees, down, up, alpha=0.1)

    for ID, strategyID in zip(jobIDsB, strategyIDs):

        data = getDataFromID(ID)
        length = data[0].shape[0]
        means = [round(table['Prop. of Cooperators'].mean(), 5) for _, table in data.items()]
        stds = [round(table['Prop. of Cooperators'].std() / np.sqrt(length), 5) for _, table in data.items()]
        up = [mean + std for mean, std in zip(means, stds)]
        down = [mean - std for mean, std in zip(means, stds)]
        axes[1][0].plot(degrees, means, label=f'$s_{strategyID}$', marker='.')
        axes[1][0].fill_between(degrees, down, up, alpha=0.1)

    # 6C ER DENSITY COMPARISON TEST

    for ID, strategyID in zip(jobIDsC, strategyIDs):

        data = getDataFromID(ID)
        length = data[0].shape[0]
        means = [round(table[f'Prop. Strategy #{strategyID}'].mean(), 5) for _, table in data.items()]
        stds = [round(table[f'Prop. Strategy #{strategyID}'].std() / np.sqrt(length), 5) for _, table in data.items()]
        up = [mean + std for mean, std in zip(means, stds)]
        down = [mean - std for mean, std in zip(means, stds)]
        axes[0][1].plot(degrees, means, label=f'$s_{strategyID}$', marker='.')
        axes[0][1].fill_between(degrees, down, up, alpha=0.1)
    # plt.xticks(degrees, [], rotation=90)

    for ID, strategyID in zip(jobIDsC, strategyIDs):

        data = getDataFromID(ID)
        length = data[0].shape[0]
        means = [round(table['Prop. of Cooperators'].mean(), 5) for _, table in data.items()]
        stds = [round(table['Prop. of Cooperators'].std() / np.sqrt(length), 5) for _, table in data.items()]
        up = [mean + std for mean, std in zip(means, stds)]
        down = [mean - std for mean, std in zip(means, stds)]
        axes[1, 1].plot(degrees, means, label=f'$s_{strategyID}$', marker='.')
        axes[1, 1].fill_between(degrees, down, up, alpha=0.1)

    labels = [f'$s_{strategyID}$' for strategyID in strategyIDs]
    axes[1][0].set_xticks(degrees)
    axes[1][0].set_xticklabels(degrees)
    axes[1][0].set_xlabel('$d$')

    axes[1][1].set_xticks(degrees)
    axes[1][1].set_xticklabels(equivalent_densities)
    axes[1][1].set_xlabel('$\lambda$')

    axes[1, 0].set_ylabel("Prop. of \nCooperators")
    axes[0, 0].set_ylabel("Prop. of \nStrategy")
    axes[0, 0].set_title("$d$-RRL")
    axes[0, 1].set_title("ER")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    lgd = axes[1][1].legend(handles, labels, loc='middle center', bbox_to_anchor=(1.1, 1.65))

    # plt.show()
    plt.savefig('test', bbox_extra_artists=(lgd,), bbox_inches='tight')
