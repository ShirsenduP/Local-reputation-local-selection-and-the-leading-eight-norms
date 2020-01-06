from CodeEvolution.models import LrGeWSSWNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment
import numpy as np

if __name__ == '__main__':

    """
    Test 11A - 0
    
    Finding the proportions of cooperation in watts-strogatz-small-world models, parameterised by rewiring 
    probability alpha ranging from 0 (regular lattice) to 1 (fully random graph). (default 4 nearest neighbours, 
    probability 0 -> 1 in steps of 0.1.

    """

    rerunSimulations = True
    repeats = 100
    var = 'smallWorld'
    values = []
    for n in np.arange(4, 4.01, 1):
        for prob in np.arange(0, 1.01, 0.1):
            values.append((int(n), round(prob, 3)))
    mainID = 2

    if rerunSimulations:

        # Default Parameters for simulations
        C = Config(size=300, initialState=State(mainID, 1, 8), mutationProbability=0.1, smallWorld=(None, None),
                   maxPeriods=5000)
        E = Experiment(networkType=LrGeWSSWNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)

        E.showExperiments()
        E.run(cluster=True)
        # E.run(display=True)
