import random

import matplotlib.pyplot as plt
import numpy as np

from CodeEvolution.models import LrGeERNetwork
from CodeEvolution.config import Config, State


class TestNetwork:

    # Set seed for reproducibility
    seed = 1  # Seed originally set to be 1
    random.seed(seed)
    np.random.seed(seed)

    # Constant parameters for all tests in this module
    config = Config(initialState=State(0, 1, 8), # d=[1,0,1,1,1,0,1,0]
                    size=6,
                    sparseDensity=True,
                    omegas=0.5,
                    maxPeriods=2,
                    delta=1,
                    mutationProbability=0)

    def setup_method(self):
        """Create preconfigured network on which each method is tested with deterministic results."""
        self.network = LrGeERNetwork(TestNetwork.config)

    def test_global_get_opponent_reputation(self):
        pass

    def test_global_update_reputation(self):
        pass

    def test_local_get_opponent_reputation(self):
        pass

    def test_local_update_reputation(self):
        # perfect reputation transfer
        # config.delta is 1

        # agent 0 interacts with agent 4
        agent0, agent4 = self.network.agentList[0], self.network.agentList[4]

        # All agent's histories are initialised as None
        # Check agent0's and agent4's neighbours know nothing about them yet
        for agent in agent0.neighbours:
            assert agent.history[agent0] is None
        for agent in agent4.neighbours:
            assert agent.history[agent4] is None

        # agent 0 will cooperate, agent 4 will cooperate
        agent0Move, agent4Move = 'C', 'C'

        # Run method
        self.network.updateReputation(agent0, agent4, 1, 1, agent0Move, agent4Move)

        # Check agent 0's neighbours know 0 is good
        for agent in agent0.neighbours:
            assert agent.history[agent0] == 1
        for agent in agent4.neighbours:
            assert agent.history[agent4] == 1
