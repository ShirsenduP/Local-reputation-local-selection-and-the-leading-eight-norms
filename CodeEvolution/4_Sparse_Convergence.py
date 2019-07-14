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

    logging.basicConfig(filename='debug.log', filemode='w', level=logging.CRITICAL)
    # logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

    """Test 4 - Sparse networks, testing the length of time til convergence."""

    rerunSimulations = True

    if rerunSimulations:
        size = 250
        sparse = 2*np.log(size)/size
        rangeOfMaxPeriods = [2000]

        """All-D versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
        ten time-steps on average."""

        pops = Experiment.generatePopulationList(proportion=1, mutantID=8)
        default = Config(size=size, initialState=State(mainID=0, proportion=1, mutantID=8),
                         mutationProbability=0.05, densities=sparse, omegas=0.99)
        E = Experiment(networkType=LrGe_Network, defaultConfig=default, repeats=20,
                       variable='population', values=pops)
        E.showExperiments()
        E.run(displayFull=True)

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
