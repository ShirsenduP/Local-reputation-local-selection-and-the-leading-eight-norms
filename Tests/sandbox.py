import random
import logging

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import CodeEvolution
from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork, GrLeERNetwork, LrLeERNetwork
from CodeEvolution.agent import GrGeAgent
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment

pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.set_option('display.width', 320)

if __name__=="__main__":

    con = Config(
        initialState=State(0,0.5,7),
        size=300,
        maxPeriods=2000,
        delta=1,
        sparseDensity=True,
        mutationProbability=0
    )
    E = Experiment(
        networkType=LrGeERNetwork,
        variable='density',
        values=[0.3, 0.4],
        defaultConfig=Config(
            size=50,
            delta=1
        ),
        repeats=2
    )

    results = E.run(export=True)

