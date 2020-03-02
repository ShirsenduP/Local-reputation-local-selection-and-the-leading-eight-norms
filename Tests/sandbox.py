import random
import logging

import numpy as np
import matplotlib.pyplot as plt

import CodeEvolution
from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork
from CodeEvolution.agent import GrGeAgent
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment

if __name__=="__main__":
    con = Config(
        initialState=State(0,1,8),
        size=10,
        maxPeriods=10,
        delta=1
    )

    net1 = GrGeERNetwork(con)
    net2 = LrGeERNetwork(con)

    net1.runSimulation()
    print(net1.results)

    net2.runSimulation()
    print(net2.results)