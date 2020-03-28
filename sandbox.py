import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork, GrLeERNetwork, LrLeERNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.experiment import Experiment

if __name__ == "__main__":

    # C = Config(
    #     size=250,
    #     initialState=State(2, 1, 8),
    #     mutationProbability=0.1,
    #     delta=1)
    #
    # variable = 'size'
    # values = [10, 50, 100, 150, 200, 250, 300, 350, 400]
    #
    # E = Experiment(
    #     networkType=GrGeERNetwork,
    #     description="Effect of size of population on the Leading 8 under Ohtsuki and Isawa",
    #     variable=variable,
    #     values=values,
    #     defaultConfig=C,
    #     repeats=10
    # )
    #
    # E.run(export=True, expName="s2_GrGe_Size")

    df = pd.read_csv("s2_GrGe_Size.csv")
    print(df)
    means = df.groupby('size').mean()

    plt.subplot()
    plt.title("Ohtsuki Isawa GrGe vs Size")
    plt.plot(means['Prop. of Cooperators'])
    plt.ylabel("Proportion of Cooperation")
    plt.xlabel("Size of Population")
    plt.show()