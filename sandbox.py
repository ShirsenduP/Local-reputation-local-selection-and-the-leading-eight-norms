import pandas as pd

from CodeEvolution.config import Config, State
from CodeEvolution.experiment import Experiment
from CodeEvolution.models import GrGeERNetwork

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 320)

if __name__ == "__main__":
    C = Config(
        size=100,
        initialState=State(0, 1, 8),
        mutationProbability=0.1,
        delta=1,
        sparseDensity=True,
        alpha=0.01,
        maxPeriods=50)

    variable = 'population'
    strats = range(3)
    values = Experiment.generatePopulationList(strats, 1, 8)

    E = Experiment(
        networkType=GrGeERNetwork,
        description="Effect of size of population on the Leading 8 under Ohtsuki and Isawa",
        variable=variable,
        values=values,
        defaultConfig=C,
        repeats=2
    )

    # E.showExperiments()
    df = E.run(export=False, expName=f"LrGe_updateProb_{0.1}")
    print(df)
