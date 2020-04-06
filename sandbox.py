import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork, GrLeERNetwork, LrLeERNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.experiment import Experiment

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 320)

if __name__ == "__main__":

    C = Config(
        size=300,
        initialState=State(0, 1, 8),
        mutationProbability=0.1,
        delta=1,
        maxPeriods=2000)

    variable = 'population'
    strats = range(8)
    values = Experiment.generateSinglePopulationProportionList(2, 8)

    E = Experiment(
        networkType=GrGeERNetwork,
        description="Effect of size of population on the Leading 8 under Ohtsuki and Isawa",
        variable=variable,
        values=values,
        defaultConfig=C,
        repeats=3
    )

    df = E.run(export=False, expName="s2_GrGe_Size")

    # # df = pd.read_csv("s2_GrGe_Size.csv")
    means = df.groupby('Mutant Initial Prop.').mean()
    sems = df.groupby('Mutant Initial Prop.').sem()
    plt.subplot()
    plt.errorbar(x=np.arange(1, 0, -0.25), y=means['Prop. of Cooperators'], yerr=sems['Prop. of Cooperators'])
    plt.ylabel("Proportion of Cooperation")
    plt.xlabel("Size of Population")
    plt.show()
    #
    # # N = LrGeERNetwork(C)
    # df = N.runSimulation()
    # print(type(df))
