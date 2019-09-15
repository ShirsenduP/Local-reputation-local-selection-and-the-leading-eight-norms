from CodeEvolution.models import LrGeWSSWNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment
import numpy as np

if __name__ == '__main__':

    """
    Test 11D - 0
    
    WSSW networks changing the original value of k prior to rewiring. Setting rewiring to 0.001 (from small world paper)
    
    """

    rerunSimulations = True
    repeats = 100
    var = 'smallWorld'
    degrees = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    values = []
    for deg in degrees:
        values.append((deg, 0.001))
    mainID = 4

    if rerunSimulations:

        # Default Parameters for simulations
        C = Config(size=300, initialState=State(mainID, 1, 8), mutationProbability=0.1, smallWorld=(None, None),
                   maxPeriods=2500)
        E = Experiment(networkType=LrGeWSSWNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)

        E.showExperiments()
        # E.run(cluster=True)
        E.run(display=True)
