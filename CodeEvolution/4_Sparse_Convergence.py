import logging
from matplotlib import pyplot as plt
import pandas as pd

from CodeEvolution.Evaluator import Evaluator
from CodeEvolution.LrLe import LrLe_Network
from CodeEvolution.config import Config
from CodeEvolution.Experiment import Experiment

if __name__ == '__main__':
    """Test 4 - MAIN RESULT -> Testing dominance of Leading 8 on sparse network with LrLe setup"""

    logging.basicConfig(filename='debug.log', filemode='w', level=logging.CRITICAL)
    # logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

    rerunSimulations = False

    if rerunSimulations:

        default = Config(size=200, sparseDensity=True, mutationProbability=0.1)

        """All-D versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
        ten time-steps on average."""
        popsD = Experiment.generatePopulationList(proportion=1, mutantID=8)
        E = Experiment(networkType=LrLe_Network, defaultConfig=default, repeats=100,
                       variable='population', values=popsD)
        E.showExperiments()
        E.run(export=True)

        """All-C versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
                ten time-steps on average."""
        popsC = Experiment.generatePopulationList(proportion=1, mutantID=9)
        E2 = Experiment(networkType=LrLe_Network, defaultConfig=default, repeats=100,
                        variable='population', values=popsC)
        E2.showExperiments()
        E2.run(export=True)

    # PLOTS
    #
    # s0 = Evaluator.open_results("LrLe_population_2019-07-18 21:32:51")  # LrLe vs All-D
    s0 = Evaluator.open_results("LrLe_population_2019-07-18 23:50:31")  # LrLe vs All-C

    s = iter(range(8))
    for thing in s0.values():
        print(thing)
        x = thing['Unnamed: 0']
        y = thing['Prop. Strategy #9']
        seriesID = next(s)
        plt.scatter(x, y, label=str(seriesID), marker=seriesID, s=40, alpha=0.3)

    plt.xlabel('Time-steps to convergence')
    plt.ylabel('Final proportion of Mutants')
    plt.legend(loc='center left')
    plt.show()

    plt.show()
    averageds0 = [frame for frame in s0.values()]
    print(pd.DataFrame(averageds0))

"""
    # Plots
    Evaluator.show_result_dir()
    LrLe_AllD = Evaluator.open_results("LrLe_population_2019-07-17 05:09")
    # LrLe_AllC = Evaluator.open_results("type_population_2019-07-07 04:30")

    LrLe_AllD_Stable_Proportion = Evaluator.getProportionOfStable(LrLe_AllD)
    # LrLe_AllC_Stable_Proportion = Evaluator.getProportionOfStable(LrLe_AllC)

    labels = Evaluator.getStrategyLabels()
    x = np.arange(len(labels))
    width = 0.13

    fig, ax = plt.subplots(figsize=(10, 3))

    rects3A = ax.bar(x + 3 * width / 2, LrLe_AllD_Stable_Proportion, width, label='LrLe_All-D')
    # rects3B = ax.bar(x + 5 * width / 2, LrLe_AllC_Stable_Proportion, width, label='LrLe_All-C')

    ax.set_title('Proportions of the leading eight that remain stable against All-C/D')
    ax.set_xticks(x)
    ax.set_ylabel('Proportion of Simulations \nwith stable strategy')

    ax.set_xticklabels(labels)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 - box.height * 0.15, box.width, box.height * 1.2])

    fig.legend(loc='lower center', bbox_to_anchor=(0.5, 0.03), fancybox=True, shadow=True, ncol=6)
    plt.show()
    # fig.savefig('Leading8_density_too_high')
"""