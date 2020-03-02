
import pytest
import random
import logging

import numpy as np
import matplotlib.pyplot as plt

import CodeEvolution
from CodeEvolution.models import GrGeERNetwork
from CodeEvolution.agent import GrGeAgent
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment


class TestBroadcast:

    # Set seed for reproducibility
    seed = 1  # Seed originally set to be 1
    random.seed(seed)
    np.random.seed(seed)

    # Constant parameters for all tests in this module
    config = Config(initialState=State(0, 1, 8),
                    size=6,
                    densities=1,
                    omegas=0.5,
                    maxPeriods=2,
                    delta=1,
                    mutationProbability=0)

    def setup_method(self):
        """Create preconfigured network on which each method is tested with deterministic results."""
        self.network = GrGeERNetwork(TestBroadcast.config)

    def test_get_opponent_reputation(self):
        """Test the base global reputation mechanism of accessing an agent's public reputation with no restriction"""

        # Setup GrGe ER Network
        self.network = GrGeERNetwork(TestBroadcast.config)

        # Check reputations
        agent1, agent2 = self.network.chooseTwoAgents()
        agent1_rep, agent2_rep = self.network.getOpponentsReputation(agent1, agent2) # 1, 0
        assert agent1_rep == agent1.currentReputation
        assert agent2_rep == agent2.currentReputation

        # Change an agents reputation
        agent1.currentReputation = 0 # previously 1
        agent2.currentReputation = 1 # previously 0

        # Check reputations
        new_agent1_rep, new_agent2_rep = self.network.getOpponentsReputation(agent1, agent2) # 0, 1
        assert new_agent1_rep == agent1.currentReputation
        assert new_agent2_rep == agent2.currentReputation






