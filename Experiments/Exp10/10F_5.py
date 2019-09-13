from CodeEvolution.models import LrGeWSSWNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment
import numpy as np

if __name__ == '__main__':

    """
    Test 10A - 0
    
    Effect of increasing the mutation rate on LrGeERNetwork to see where the threshold is for mutation to dominate
    Range from 0.1, 0.5 - 10 in 0.5 increments. Recall this parameter represents the expected number of 
    mutations/time-step.

    """

    rerunSimulations = True
    repeats = 100
    var = 'mutationProbability'
    values = list(np.arange(0, 10.01, 1))
    mainID = 5

    if rerunSimulations:

        # Default Parameters for simulations
        C = Config(size=300, initialState=State(mainID, 1, 8), mutationProbability=0.1, smallWorld=(4, 0.001),
                   maxPeriods=2500)
        E = Experiment(networkType=LrGeWSSWNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)

        E.showExperiments()
        E.run(cluster=True)
