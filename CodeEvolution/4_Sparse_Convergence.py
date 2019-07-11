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

    """Test 4 - Sparse networks, testing the length of time til convergence."""

    rerunSimulations = False

    if rerunSimulations:
        size = 500
        sparse = 2 * np.log(size) / size
        rangeOfMaxPeriods = list(np.arange(250, 2250, 200))

        """All-D versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
        ten time-steps on average."""

        default = Config(size=size, initialState=State(mainID=0, proportion=1, mutantID=8),
                         mutationProbability=0.1, densities=sparse)
        E = Experiment(networkType=LrGe_Network, defaultConfig=default, repeats=30,
                       variable='maxPeriods', values=rangeOfMaxPeriods)
        E.showExperiments()
        E.run(export=True)

    # PLOTS
    #
    s0 = Evaluator.open_results("LrGe_maxPeriods_2019-07-12 00:03")


    for thing in s0.values():
        print(thing)
        x = thing['Unnamed: 0']
        y = thing['Prop. Strategy #8']
        plt.scatter(x, y)
        # plt.show()

    plt.show()
    # averageds0 = [frame for frame in s0.values()]
    # print(pd.DataFrame(averageds0))
