from CodeEvolution.models import LrGeRRLNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment
from CodeEvolution.Evaluator import Evaluator as E

if __name__ == '__main__':

    """Test 6 - Strategy 0 vs All-D. Testing d-Regular Random Lattices with d = [3, 4, ..., 10]."""

    rerunSimulations = False
    repeats = 100

    # Testing degree(density)
    var = 'degree'
    values = [3, 4, 5, 6, 7, 8, 9, 10]
    mainID = 0

    if rerunSimulations:

        # Run each experiment for each of the leading 8
        # Default Parameters for simulations
        C = Config(size=200, sparseDensity=True, mutationProbability=0.1, maxPeriods=2000,
                   initialState=State(mainID=mainID, proportion=1, mutantID=8))
        E = Experiment(networkType=LrGeRRLNetwork, defaultConfig=C, repeats=repeats,
                       variable=var, values=values)
        E.showExperiments()
        E.run(export=True)

    strategy0 = E.open_results("LrGeRRL_degree_2019-08-07 13:26:23")
    # strategy0 = E.plotAllStrategiesSummary(title="", dataPath="LrGeRRL_degree_2019-08-07 13:26:23", mutantID=8)
    print(strategy0[0])

# TODO Rename script name from dominance to degree

