import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork, GrLeERNetwork, LrLeERNetwork
from CodeEvolution.config import Config, State
from CodeEvolution.experiment import Experiment

pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.set_option('display.width', 320)

desc = """
Experiment #TEST

How does delta (probability of reputation broadcast) effect levels of cooperation in the network? 

Delta  - [0, 0.1, 0.2, ..., 0.9, 1.0]
Strategy 0

"""

if __name__=="__main__":

    con = Config(
        initialState=State(0,1,8),
        size=300,
        maxPeriods=3000,
        sparseDensity=True,
        mutationProbability=0.1
    )

    # N =
