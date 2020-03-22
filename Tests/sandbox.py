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

if __name__=="__main__":
    con = Config(
        initialState=State(3,1,8),
        size=100,
        maxPeriods=100,
        delta=1,
        sparseDensity=True
    )
    #
    # fig, ax = plt.subplots(2,2)
    #
    net3 = GrLeERNetwork(con)
    # plt.sca(ax[0,0])
    # net3.getPlot()
    # plt.title("grle")
    #
    net2 = LrGeERNetwork(con)
    # plt.sca(ax[0,1])
    # net2.getPlot()
    # plt.title("lrge")
    #
    net4 = LrLeERNetwork(con)
    # plt.sca(ax[1,0])
    # net4.getPlot()
    # plt.title("lrle")
    #
    net1 = GrGeERNetwork(con)
    # plt.sca(ax[1, 1])
    # net1.getPlot()
    # plt.title("grge")

    # plt.show()

    # net1.runSimulation()
    # net2.runSimulation()
    # net3.runSimulation()
    # net4.runSimulation()

    E = Experiment(
        networkType=LrGeERNetwork,
        variable='density',
        values=[0.6, 0.8],
        defaultConfig=Config(
            size=10,
            delta=1
        ),
        repeats=3
    )

    E.run(display=True)