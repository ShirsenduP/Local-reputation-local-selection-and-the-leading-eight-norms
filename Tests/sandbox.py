import random
import logging

import numpy as np
import matplotlib.pyplot as plt

import CodeEvolution
from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork, GrLeERNetwork, LrLeERNetwork
from CodeEvolution.agent import GrGeAgent
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment

if __name__=="__main__":
    con = Config(
        initialState=State(0,1,8),
        size=10,
        maxPeriods=100,
        delta=1,
        sparseDensity=True
    )

    print(con)

    fig, ax = plt.subplots(2,2)

    net3 = GrLeERNetwork(con)
    plt.sca(ax[0,0])
    net3.getPlot()
    plt.title("grle")

    net2 = LrGeERNetwork(con)
    plt.sca(ax[0,1])
    net2.getPlot()
    plt.title("lrge")

    net4 = LrLeERNetwork(con)
    plt.sca(ax[1,0])
    net4.getPlot()
    plt.title("lrle")

    net1 = GrGeERNetwork(con)
    plt.sca(ax[1, 1])
    net1.getPlot()
    plt.title("grge")

    plt.show()





    # net1.runSimulation()
    # net2.runSimulation()
    # net3.runSimulation()
    # net4.runSimulation()

    # print(net4.results)

