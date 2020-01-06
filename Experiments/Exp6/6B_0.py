from CodeEvolution.models import LrGeRRLNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment


if __name__ == '__main__':

    """
    Effect of degree on regular random lattice on proportions of cooperation
    Strategy i = [0,1,6,7] vs degree d = [3, 10, 25, 50, 100, 200, 299], LrGe, ONLY TEN REPEATS
    """

    rerunSimulations = True
    repeats = 5


    # Testing degree(density)
    var = 'degree'
    values = [3, 10, 25, 50, 100, 200, 299]
    mainID = 0

    if rerunSimulations:

        # Run each experiment for each of the leading 8
        # Default Parameters for simulations
        C = Config(size=300, mutationProbability=0.1, maxPeriods=2500,
                   initialState=State(mainID=mainID, proportion=1, mutantID=8))
        E = Experiment(networkType=LrGeRRLNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)
        E.showExperiments()
        E.run(cluster=True)
