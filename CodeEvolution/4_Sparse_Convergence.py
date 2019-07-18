import logging
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from CodeEvolution.Evaluator import Evaluator
from CodeEvolution.GrGe import GrGe_Network
from CodeEvolution.LrGe import LrGe_Network
from CodeEvolution.LrLe import LrLe_Network
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment
from CodeEvolution.Experiment import Population

if __name__ == '__main__':

    logging.basicConfig(filename='debug.log', filemode='w', level=logging.INFO)
    # logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

    """Test 4 - Sparse networks, testing the length of time til convergence."""

    rerunSimulations = True

    if rerunSimulations:

        default = Config(size=50, sparseDensity=True, mutationProbability=0.3)

        """All-D versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
        ten time-steps on average."""
        popsD = Experiment.generatePopulationList(strategies=(0,),proportion=0.9, mutantID=8)
        E = Experiment(networkType=LrLe_Network, defaultConfig=default, repeats=400,
                       variable='population', values=popsD)
        E.showExperiments()
        E.run(display=True)

        """All-C versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
                ten time-steps on average."""
        # popsC = Experiment.generatePopulationList(proportion=1, mutantID=9)
        # E2 = Experiment(networkType=LrLe_Network, defaultConfig=default, repeats=50,
        #                 variable='population', values=popsC)
        # E2.showExperiments()
        # E2.run(export=True)
        
        

    # PLOTS
    #
    # s0 = Evaluator.open_results("LrLe_population_2019-07-17 05:09")
    #
    # for thing in s0.values():
    #     print(thing)
    #     x = thing['Unnamed: 0']
    #     y = thing['Prop. Strategy #8']
    #     plt.scatter(x, y)
    #     # plt.show()
    #
    # plt.show()
    # averageds0 = [frame for frame in s0.values()]
    # print(pd.DataFrame(averageds0))

    # Plots
    # Evaluator.show_result_dir()
    # LrLe_AllD = Evaluator.open_results("LrLe_population_2019-07-17 05:09")
    # # LrLe_AllC = Evaluator.open_results("type_population_2019-07-07 04:30")
    #
    # LrLe_AllD_Stable_Proportion = Evaluator.getProportionOfStable(LrLe_AllD)
    # # LrLe_AllC_Stable_Proportion = Evaluator.getProportionOfStable(LrLe_AllC)
    #
    # labels = Evaluator.getStrategyLabels()
    # x = np.arange(len(labels))
    # width = 0.13
    #
    # fig, ax = plt.subplots(figsize=(10, 3))
    #
    # rects3A = ax.bar(x + 3 * width / 2, LrLe_AllD_Stable_Proportion, width, label='LrLe_All-D')
    # # rects3B = ax.bar(x + 5 * width / 2, LrLe_AllC_Stable_Proportion, width, label='LrLe_All-C')
    #
    # ax.set_title('Proportions of the leading eight that remain stable against All-C/D')
    # ax.set_xticks(x)
    # ax.set_ylabel('Proportion of Simulations \nwith stable strategy')
    #
    # ax.set_xticklabels(labels)
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0 - box.height * 0.15, box.width, box.height * 1.2])
    #
    # fig.legend(loc='lower center', bbox_to_anchor=(0.5, 0.03), fancybox=True, shadow=True, ncol=6)
    # plt.show()
    # # fig.savefig('Leading8_density_too_high')
