import logging
from matplotlib import pyplot as plt
import pandas as pd

from CodeEvolution.Evaluator import Evaluator
from CodeEvolution.network import LrGeNetwork
from CodeEvolution.config import Config
from CodeEvolution.Experiment import Experiment

logging.basicConfig(filename='debug.log', filemode='w', level=logging.CRITICAL)

if __name__ == '__main__':
    """Test 5 - MAIN RESULT -> Testing dominance of Leading 8 on sparse network with LrGe setup"""

    rerunSimulations = False

    if rerunSimulations:

        # Default Parameters for simulations
        default = Config(size=200, sparseDensity=True, mutationProbability=0.1)

        """All-D versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
        ten time-steps on average."""
        popsD = Experiment.generatePopulationList(proportion=1, mutantID=8)
        E = Experiment(networkType=LrGeNetwork, defaultConfig=default, repeats=100,
                       variable='population', values=popsD)
        E.showExperiments()
        E.run(export=True)

        """All-C versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
                ten time-steps on average."""
        popsC = Experiment.generatePopulationList(proportion=1, mutantID=9)
        E2 = Experiment(networkType=LrGeNetwork, defaultConfig=default, repeats=100,
                        variable='population', values=popsC)
        E2.showExperiments()
        E2.run(export=True)

    # PLOTS

    Evaluator.plotAllStrategies(title='Leading Eight Strategies with Local Reputation and Global Evolution vs All-D',
                                dataPath='LrGe_population_2019-07-18 21:35:02', mutantID=8, save=True)
    Evaluator.plotAllStrategiesSummary(title='Leading Eight Strategies with Local Reputation and Global Evolution vs '
                                             'All-D_',
                                       dataPath='LrGe_population_2019-07-18 21:35:02', mutantID=8, save=True)
    Evaluator.plotAllStrategies(title='Leading Eight Strategies with Local Reputation and Global Evolution vs All-C',
                                dataPath='LrGe_population_2019-07-18 23:24:50', mutantID=9, save=True)
    Evaluator.plotAllStrategiesSummary(title='Leading Eight Strategies with Local Reputation and Global Evolution vs '
                                             'All-C_',
                                       dataPath='LrGe_population_2019-07-18 23:24:50', mutantID=9, save=True)


