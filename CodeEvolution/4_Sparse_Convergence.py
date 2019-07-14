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
        size = 2
        sparse = 2*np.log(size)/size
        rangeOfMaxPeriods = [2000]

        """All-D versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
        ten time-steps on average."""

        # pops = Experiment.generatePopulationList(strategies=(0,), proportion=1, mutantID=9)
        default = Config(size=size, initialState=State(mainID=0, proportion=1, mutantID=9),
                         densities=sparse, omegas=0.9)
        E = Experiment(networkType=LrGe_Network, defaultConfig=default, repeats=10,
                       variable='mutationProbability', values=[0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3])
        E.showExperiments()
        E.run(display=True)

    # PLOTS
    #
    # s0 = Evaluator.open_results("LrGe_maxPeriods_2019-07-12 00:03")
    #
    # for thing in s0.values():
    #     print(thing)
    #     x = thing['Unnamed: 0']
    #     y = thing['Prop. Strategy #8']
    #     plt.scatter(x, y)
    #     # plt.show()
    #
    # plt.show()
    # # averageds0 = [frame for frame in s0.values()]
    # # print(pd.DataFrame(averageds0))
