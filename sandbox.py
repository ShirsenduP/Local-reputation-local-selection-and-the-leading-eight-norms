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
        size=250,
        initialState=State(2, 1, 8),
        mutationProbability=0.1,
        delta=1,
        maxPeriods=500)

    variable = 'size'
    # values = list(range(10, 52, 2))
    values = [400]

    E = Experiment(
        networkType=GrGeERNetwork,
        description="Effect of size of population on the Leading 8 under Ohtsuki and Isawa",
        variable=variable,
        values=values,
        defaultConfig=C,
        repeats=2
    )

    df = E.run(export=False, expName="s2_GrGe_Size")

    print(df)
    #
    # # df = pd.read_csv("s2_GrGe_Size.csv")
    # means = df.groupby('size').mean()['Prop. of Cooperators']
    # sems = df.groupby('size').sem()['Prop. of Cooperators']
    #
    # plt.subplot()
    # # plt.plot(means['Prop. of Cooperators'])
    # plt.errorbar(values, means, yerr=sems)
    # plt.ylabel("Proportion of Cooperation")
    # plt.xlabel("Size of Population")
    # plt.show()
