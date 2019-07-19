import logging
from matplotlib import pyplot as plt
import pandas as pd

from CodeEvolution.Evaluator import Evaluator
from CodeEvolution.LrGe import LrGe_Network
from CodeEvolution.config import Config
from CodeEvolution.Experiment import Experiment

if __name__ == '__main__':
    """Test 5 - MAIN RESULT -> Testing dominance of Leading 8 on sparse network with LrGe setup"""

    logging.basicConfig(filename='debug.log', filemode='w', level=logging.CRITICAL)
    # logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

    rerunSimulations = False

    if rerunSimulations:

        default = Config(size=200, sparseDensity=True, mutationProbability=0.1)

        """All-D versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
        ten time-steps on average."""
        popsD = Experiment.generatePopulationList(proportion=1, mutantID=8)
        E = Experiment(networkType=LrGe_Network, defaultConfig=default, repeats=100,
                       variable='population', values=popsD)
        E.showExperiments()
        E.run(export=True)

        """All-C versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
                ten time-steps on average."""
        popsC = Experiment.generatePopulationList(proportion=1, mutantID=9)
        E2 = Experiment(networkType=LrGe_Network, defaultConfig=default, repeats=100,
                        variable='population', values=popsC)
        E2.showExperiments()
        E2.run(export=True)

    # PLOTS

    s0 = Evaluator.open_results("LrGe_population_2019-07-18 21:35:02")
    # s0 = Evaluator.open_results("LrGe_population_2019-07-18 23:24:50")
    s = iter(range(8))
    for thing in s0.values():
        print(thing)
        x = thing['Unnamed: 0']
        y = thing['Prop. Strategy #8']
        seriesID = next(s)
        plt.scatter(x, y, label=str(seriesID), marker=seriesID, s=40, alpha=0.3)

    plt.xlabel('Time-steps to convergence')
    plt.ylabel('Final proportion of Mutants')
    plt.legend(loc='center left')
    plt.show()
    averageds0 = [frame for frame in s0.values()]
    print(pd.DataFrame(averageds0))
