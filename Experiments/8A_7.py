from CodeEvolution.models import LrGePLNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment

if __name__ == '__main__':

    """
    Test 8A - 7
    Effect of parameter of attachment on the a scale-free network (Barabasi Albert model), 
    """

    rerunSimulations = True
    repeats = 100
    var = 'attachment'
    values = list(range(2, 11, 1))
    mainID = 7

    if rerunSimulations:

        # Default Parameters for simulations
        C = Config(size=300, initialState=State(mainID, 1, 8), mutationProbability=0.1, maxPeriods=5000)
        E = Experiment(networkType=LrGePLNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)

        E.showExperiments()
        E.run(cluster=True)


