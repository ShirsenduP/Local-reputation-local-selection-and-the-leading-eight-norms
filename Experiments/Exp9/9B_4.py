from CodeEvolution.models import LrGeERNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment

if __name__ == '__main__':

    """
    Test 9A - 0
    
    Effect of simulation on variance of convergence point, Erdos Renyi network, size 300, test maxT from 500-5000 at
    intervals of 250 to see if maxT of 5000 is necessary for every simulation.
    """

    rerunSimulations = True
    repeats = 100
    var = 'maxPeriods'
    values = list(range(500, 5001, 250))
    mainID = 4

    if rerunSimulations:

        # Default Parameters for simulations
        C = Config(size=300, initialState=State(mainID, 1, 8), mutationProbability=0.1, sparseDensity=True)
        E = Experiment(networkType=LrGeERNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)

        E.showExperiments()
        E.run(cluster=True)
