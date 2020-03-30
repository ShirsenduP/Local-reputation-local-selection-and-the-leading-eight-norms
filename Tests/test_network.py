
import pytest
import random
import logging

import numpy as np
import matplotlib.pyplot as plt

import CodeEvolution
from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork
from CodeEvolution.agent import GrGeAgent
from CodeEvolution.config import Config, State
from CodeEvolution.experiment import Experiment


class TestNetwork:

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
        self.network = GrGeERNetwork(TestNetwork.config)

    def test_get_opponent_reputation(self):
        """Test the base global reputation mechanism of accessing an agent's public reputation with no restriction"""

        # Setup GrGe ER Network
        self.network = GrGeERNetwork(TestNetwork.config)

        # Check reputations
        agent1, agent2 = self.network.chooseAgents()
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

    def test_correct_network_generation(self):

        # force network generation with density too low
        with pytest.raises(Exception):
            config = Config(size=100, densities=0.01)
            N = LrGeERNetwork(config)

        # # force network generation with too few agents
        # with pytest.raises(Exception):
        #     config = Config(size=1)
        #     N = LrGeERNetwork(config)
        #
        # # force network generation with uneven strategy proportions
        # with pytest.raises(Exception):
        #     config = Config(size=10, initialState=State(0, 0.05, 8))
        #     N = LrGeERNetwork(config)

    def test_networkFromAdjacencyMatrix(self):
        """Test the generation of a Network Object when given an adjacency matrix"""
        assert(1==1)

    def test_networkDensity(self):
        """Make sure that the specified config.densities is close enough to the actual network density"""
