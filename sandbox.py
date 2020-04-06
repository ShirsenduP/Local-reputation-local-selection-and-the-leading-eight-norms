import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork, GrLeERNetwork, LrLeERNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.experiment import Experiment

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 320)

if __name__ == "__main__":

    for alpha in [0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.99]:
        C = Config(
            size=300,
            initialState=State(0, 1, 8),
            mutationProbability=0.1,
            delta=1,
            sparseDensity=True,
            updateProbability=alpha,
            maxPeriods=2000)

        variable = 'population'
        strats = range(8)
        values = Experiment.generatePopulationList(range(8), 1, 8)
        # values = Experiment.generateSinglePopulationProportionList(8, 8)

        E = Experiment(
            networkType=LrGeERNetwork,
            description="Effect of size of population on the Leading 8 under Ohtsuki and Isawa",
            variable=variable,
            values=values,
            defaultConfig=C,
            repeats=20
        )

        E.showExperiments()
        df = E.run(export=True, expName=f"LrGe_updateProb_{alpha}")
        means = df.groupby('Main ID').mean()
        sems = df.groupby('Main ID').sem()

        plt.subplot()
        plt.errorbar(x=strats, y=means['Prop. of Cooperators'], yerr=sems['Prop. of Cooperators'], label=f"{alpha}")
        plt.ylabel("Proportion of Cooperation")
        plt.xlabel("Strategy")

    plt.legend()
    plt.show()
