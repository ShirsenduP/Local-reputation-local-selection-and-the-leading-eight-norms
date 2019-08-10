from CodeEvolution.models import LrGeERNetwork
from CodeEvolution.config import Config
from CodeEvolution.Experiment import Experiment

if __name__ == '__main__':

    """
    Test 7
    Reconfirming all preliminary results. LrGe dominance of leading eight strategies on ER random network 
    against All-D.
    """

    rerunSimulations = True
    repeats = 100
    var = 'population'
    values = Experiment.generatePopulationList(proportion=1, mutantID=8)

    if rerunSimulations:

        # Default Parameters for simulations
        C = Config(size=500, mutationProbability=0.1, maxPeriods=5000)
        E = Experiment(networkType=LrGeERNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)

        E.showExperiments()
        E.run(cluster=True)
