from CodeEvolution.models import LrGeERNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment
import numpy as np

if __name__ == '__main__':

    """
    Test 13A - 0
    
    The effect of the probability of broadcast of information to an agent's neighbours following an interaction.

    """

    rerunSimulations = True
    repeats = 100
    mainID = 0
    var = 'delta'
    values = [round(0.1*i,2) for i in range(11)]

    if rerunSimulations:

        # Default Parameters for simulations
        C = Config(size=300, mutationProbability=0, sparseDensity=True, maxPeriods=2500)
        E = Experiment(networkType=LrGeERNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)
        E.showExperiments()
        E.run(cluster=True)
        # E.run(display=True)