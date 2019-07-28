import os
import logging
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from CodeEvolution.Evaluator import Evaluator
from CodeEvolution.network import GrGe_Network, LrGe_Network, LrLe_Network
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment
from CodeEvolution.Experiment import Population

if __name__ == '__main__':

    # logging.basicConfig(filename='debug.log', filemode='w', level=logging.CRITICAL)
    # logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

    """Test 6 -"""

    rerunSimulations = True

    with open('test.txt', 'w') as file:
        s1 = str(os.getcwd())
        s2 = str(os.listdir())
        file.write(s1)
        file.write(s2)

    if rerunSimulations:
        default = Config(size=200, sparseDensity=True, mutationProbability=0.1)

        """All-D versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
        ten time-steps on average."""
        popsD = Experiment.generatePopulationList(strategies=(1, 5), proportion=1, mutantID=8)
        E = Experiment(networkType=LrGe_Network, defaultConfig=default, repeats=3,
                       variable='population', values=popsD)
        E.showExperiments()
        E.run(cluster=True)



        """All-C versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
                ten time-steps on average."""
        # popsC = Experiment.generatePopulationList(proportion=1, mutantID=8)
        # E2 = Experiment(networkType=LrGe_Network, defaultConfig=default, repeats=1,
        #                 variable='density', values=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
        # E2.showExperiments()
        # E2.run(display=True)

    # PLOTS
    #
    # s0 = Evaluator.open_results("LrLe_population_2019-07-17 05:28")
    #
    # for thing in s0.values():
    #     print(thing)
    #     x = thing['Unnamed: 0']
    #     y = thing['Prop. Strategy #9']
    #     plt.scatter(x, y)
    #     # plt.show()
    #
    # plt.show()
    # # averageds0 = [frame for frame in s0.values()]
    # # print(pd.DataFrame(averageds0))
