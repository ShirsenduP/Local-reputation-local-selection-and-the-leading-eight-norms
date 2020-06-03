import random

import pytest

from ..opgar import Configuration

random.seed(0)


@pytest.fixture(scope="session")
def test_config():
    C = Configuration(population_size=100, pgg_size=4, technology=2, rounds=15, composition={
        "I": 1 / 3,
        "II": 1 / 3,
        "III": 1 / 3
    }, norm=None)
    return C


@pytest.fixture(scope="session")
def test_config2():
    C = Configuration(population_size=4, pgg_size=4, technology=1.5, rounds=1, composition={
            "III": 3 / 4,
            "X": 1 / 4
        }, norm="Loner")
    return C


@pytest.fixture(scope="session")
def test_config3():
    C1 = Configuration(population_size=100, pgg_size=7, technology=2, rounds=10, composition={
            "I": 1 / 3,
            "II": 1 / 3,
            "III": 1 / 3
        }, norm=None)
    C2 = Configuration(population_size=100, pgg_size=4, technology=2, rounds=10, composition={
            "I": 1 / 3,
            "II": 1 / 3,
            "III": 1 / 4
        }, norm=None)
    C3 = Configuration(population_size=-100, pgg_size=-4, technology=0.5, rounds=-10, composition={
            "I": 1 / 3,
            "II": 1 / 3,
            "III": 1 / 3
        }, norm=None)
    C4 = Configuration(population_size=100, pgg_size=4, technology=2, rounds=10, composition={
            "I": 1 / 3,
            "II": 3 / 3,
            "III": -1 / 3
        }, norm=None)
    C5 = Configuration(population_size=3, pgg_size=3, technology=2, rounds=10, composition={
            "I": 1 / 3,
            "II": 1 / 3,
            "III": 1 / 3
        }, norm=None)
    C6 = Configuration(population_size=30, pgg_size=2, technology=2, rounds=10, composition={
            "I": 1 / 3,
            "II": 1 / 3,
            "III": 1 / 3
        }, norm=None)
    invalid_configs = [C1, C2, C3, C4, C5, C6]
    return invalid_configs
