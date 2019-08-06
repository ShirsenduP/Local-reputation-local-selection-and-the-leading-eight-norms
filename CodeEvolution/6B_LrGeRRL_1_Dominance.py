from CodeEvolution.network import LrGeRRLNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment

if __name__ == '__main__':

    """Test 6 - Strategy 0 vs All-D. Testing d-Regular Random Lattices with d = [3, 4, ..., 10]."""

    rerunSimulations = True
    repeats = 100

    # Testing degree(density)
    var = 'degree'
    values = [3, 4, 5, 6, 7, 8, 9, 10]
    mainID = 1

    if rerunSimulations:

        # Run each experiment for each of the leading 8
        # Default Parameters for simulations
        C = Config(size=200, sparseDensity=True, mutationProbability=0.1, maxPeriods=2000,
                   initialState=State(mainID=mainID, proportion=1, mutantID=8))
        E = Experiment(networkType=LrGeRRLNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)
        E.showExperiments()
        E.run(cluster=True)
