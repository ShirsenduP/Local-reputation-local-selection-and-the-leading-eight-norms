from CodeEvolution.models import LrGeRRLNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment

if __name__ == '__main__':

    """
    Test 8B - 0
    Local Reputation and Global Evolution vs All D for L4 strategies against size of network
    """

    rerunSimulations = True
    repeats = 100
    var = 'size'
    values = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    mainID = 4

    if rerunSimulations:

        # Default Parameters for simulations
        C = Config(initialState=State(mainID, 1, 8), mutationProbability=0.1, maxPeriods=2500,
                   degree=4)
        E = Experiment(networkType=LrGeRRLNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)
        E.checkDensitiesForSize()
        E.showExperiments()
        E.run(cluster=True)
