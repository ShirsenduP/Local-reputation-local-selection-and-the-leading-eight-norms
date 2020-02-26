
import pytest
import random
import logging

import numpy as np

from CodeEvolution.models import GrGeERNetwork
from CodeEvolution.agent import GrGeAgent
from CodeEvolution.config import Config, State
from CodeEvolution.Experiment import Experiment


class TestBroadcast:

    @classmethod
    def setup_class(cls):
        """Create default Config on which every process is deterministic."""
        logging.info("setup class")
        seed = 1
        random.seed(seed)
        np.random.seed(seed)

    def setup_method(self):
        """Create preconfigured network on which each method is tested with deterministic results."""
        print("setup test")

    @classmethod
    def teardown_class(cls):
        """Tear down the test Config after testing instance complete."""
        print("tear down class")

    def teardown_method(self):
        """Destroy preconfigured network following each test."""
        print("teardown test")

    def test_setupandteardown(self):
        """Example test 1"""
        assert 1 == 1

    def test_2(self):
        """Example test 2"""
        assert 2 == 2
