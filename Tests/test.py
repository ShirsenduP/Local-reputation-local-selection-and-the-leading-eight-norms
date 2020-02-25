from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import random

from CodeEvolution.models import GrGeERNetwork
from CodeEvolution.agent import GrGeAgent
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment

# random.seed(1)
# np.random.seed(1)
import pandas as pd
desired_width = 640
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)


if __name__ == '__main__':
    var = 'population'
    values = Experiment.generatePopulationList(
        strategies=range(2, 6), proportion=1)

    C = Config(size=150, mutationProbability=0.1, maxPeriods=50, delta=1)
    E = Experiment(networkType=GrGeERNetwork, defaultConfig=C,
                   repeats=10, variable=var, values=values)
    E.showExperiments()
    E.run(display=True)
