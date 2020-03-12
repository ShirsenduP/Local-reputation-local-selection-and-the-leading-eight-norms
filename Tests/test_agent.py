
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

class TestAgent:

    def test_check_equality(self):
        """Check if two agents are the same."""

        agent0 = GrGeAgent(0, 0)
        agent1 = GrGeAgent(1, 0)
        assert agent0 != agent1
        assert agent0 == agent0

    def test_agent_reference(self):
        """Ensure that agents are not being copied."""

        agent1 = GrGeAgent(0,1)
        agent2 = GrGeAgent(1,1)
        agent2.neighbours.append(agent1)
        agent1.neighbours.append(agent2)

        assert agent2.neighbours[0] == agent1
        assert id(agent2.neighbours[0]) == id(agent1)
        assert agent1.neighbours[0] == agent2
        assert id(agent1.neighbours[0]) == id(agent2)

        del agent1, agent2
