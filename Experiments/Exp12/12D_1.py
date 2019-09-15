from CodeEvolution.models import LrGeRRLNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment
import numpy as np

if __name__ == '__main__':

    """
    Test 12B - 0
    
    Allowing no mutation, but modulating the initial proportion of mutants in the population to find the limiting point
    of where the network can recover. Range 0-1 in 0.05 increments. Taking Tmax to 3000 as time to convergence has 
    little effect on simulations.

    """

    rerunSimulations = True
    repeats = 100
    mainID = 1
    var = 'population'
    values = Experiment.generateSinglePopulationProportionList(mainID, 8)

    if rerunSimulations:

        # Default Parameters for simulations
        C = Config(size=300, mutationProbability=0, sparseDensity=True, maxPeriods=2500, degree=4)
        E = Experiment(networkType=LrGeRRLNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)
        E.showExperiments()
        E.run(cluster=True)
