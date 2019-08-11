import logging
from matplotlib import pyplot as plt
import pandas as pd

from CodeEvolution.Evaluator import Evaluator
from CodeEvolution.models import LrLeERNetwork
from CodeEvolution.config import Config
from CodeEvolution.Experiment import Experiment

logging.basicConfig(filename='debug.log', filemode='w', level=logging.CRITICAL)

if __name__ == '__main__':
    """Test 4 - MAIN RESULT -> Testing dominance of Leading 8 on sparse network with LrLe setup"""

    rerunSimulations = True

    if rerunSimulations:

        # Default Parameters for simulations
        default = Config(size=200, sparseDensity=True, mutationProbability=0.1)

        """All-D versus all strategies, 100/0 initial proportion, expected mutant every 10 time-steps."""
        popsD = Experiment.generatePopulationList(proportion=1, mutantID=8)
        E = Experiment(networkType=LrLeERNetwork, defaultConfig=default, repeats=100,
                       variable='population', values=popsD)
        E.showExperiments()
        E.run(export=True)

        """All-C versus all strategies, 100/0 initial proportion, expected mutant every 10 time-steps."""
        popsC = Experiment.generatePopulationList(proportion=1, mutantID=9)
        E2 = Experiment(networkType=LrLeERNetwork, defaultConfig=default, repeats=100,
                        variable='population', values=popsC)
        E2.showExperiments()
        E2.run(export=True)

    # Plots

    # Evaluator.plotAllStrategiesSummary(title='Leading Eight Strategies with Local Reputation and Local Evolution vs '
    #                                    'All-D_', dataPath="LrLe_population_2019-07-18 21:32:51", mutantID=8, save=True)
    #
    # Evaluator.plotAllStrategiesSummary(title='Leading Eight Strategies with Local Reputation and Local Evolution vs '
    #                                    'All-C_', dataPath="LrLe_population_2019-07-18 23:50:31", mutantID=9, save=True)
    #
    # Evaluator.plotAllStrategies(title="Leading Eight Strategies with Local Reputation and Local Evolution vs All-C",
    #                             dataPath="LrLe_population_2019-07-18 23:50:31", mutantID=9, save=True)
    #
    # Evaluator.plotAllStrategies(title="Leading Eight Strategies with Local Reputation and Local Evolution vs All-D",
    #                             dataPath="LrLe_population_2019-07-18 21:32:51", mutantID=8, save=True)

    default = Config(size=200, sparseDensity=True, mutationProbability=0.1)

    print(default)
