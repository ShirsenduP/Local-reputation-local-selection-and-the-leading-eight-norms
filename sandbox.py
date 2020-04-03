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
        size=550,
        initialState=State(3, 1, 8),
        mutationProbability=0.1,
        delta=1,
        maxPeriods=5000)

    variable = 'size'
    values = list(range(10, 500, 50))
    # values = [600]

    E = Experiment(
        networkType=LrLeERNetwork,
        description="Effect of size of population on the Leading 8 under Ohtsuki and Isawa",
        variable=variable,
        values=values,
        defaultConfig=C,
        repeats=6
    )

    df = E.run(export=False, expName="s2_GrGe_Size")
    # TODO: Why does Group II suddenly work now on GrGe at large N?
    print(df)
    #
    # # df = pd.read_csv("s2_GrGe_Size.csv")
    means = df.groupby('size').mean()['Prop. of Cooperators']
    sems = df.groupby('size').sem()['Prop. of Cooperators']

    plt.subplot()
    # plt.plot(means['Prop. of Cooperators'])
    plt.errorbar(values, means, yerr=sems)
    plt.ylabel("Proportion of Cooperation")
    plt.xlabel("Size of Population")
    plt.show()
