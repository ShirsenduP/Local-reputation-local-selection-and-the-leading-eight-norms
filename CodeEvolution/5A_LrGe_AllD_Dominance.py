import logging
from matplotlib import pyplot as plt
import pandas as pd

from CodeEvolution.Evaluator import Evaluator
from CodeEvolution.network import LrGeNetwork
from CodeEvolution.config import Config
from CodeEvolution.Experiment import Experiment

logging.basicConfig(filename='debug.log', filemode='w', level=logging.CRITICAL)

if __name__ == '__main__':
    """Test 5 - MAIN RESULT -> Testing dominance of Leading 8 on sparse network with LrGe setup VS ALL-D"""

    rerunSimulations = True
    repeats = 100

    if rerunSimulations:

        # Default Parameters for simulations
        default = Config(size=200, sparseDensity=True, mutationProbability=0.1)

        """All-D versus all the populations, initially weighted at 0/100 and mutations occurring randomly once every 
        ten time-steps on average."""
        pops = Experiment.generatePopulationList(proportion=1, mutantID=8)
        E = Experiment(networkType=LrGeNetwork, defaultConfig=default, repeats=repeats,
                       variable='population', values=pops)
        E.showExperiments()
        E.run(cluster=True)
