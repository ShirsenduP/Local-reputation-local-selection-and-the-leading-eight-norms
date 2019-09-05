import logging

from CodeEvolution.models import LrGeERNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment
from CodeEvolution.structures import RandomRegularLattice as RRL


if __name__ == '__main__':

    """
    Effect of equivalent density on Erdos Renyi random network, LrGe from RRL degrees
    Strategy i = [0,1,6,7] vs degree d = [3, 10, 25, 50, 100, 200, 299], LrGe, ONLY TEN REPEATS
    """

    rerunSimulations = True
    repeats = 5

    # degrees = [10, 100, 200, 299]
    degrees = [3, 25, 50]

    # Testing density (from degree)
    var = 'density'
    values = []
    mainID = 0
    for d in degrees:
        config = Config(size=300, degree=d)
        values.append(RRL.getTheoreticalDensity(config))

    if rerunSimulations:

        # Run each experiment for each of the leading 8
        # Default Parameters for simulations
        C = Config(size=300, mutationProbability=0.1, maxPeriods=2500,
                   initialState=State(mainID=mainID, proportion=1, mutantID=8))
        E = Experiment(networkType=LrGeERNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)
        E.showExperiments()
        E.run(cluster=True)
