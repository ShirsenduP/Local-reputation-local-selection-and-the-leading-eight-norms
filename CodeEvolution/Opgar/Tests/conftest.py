import pytest
import random

random.seed(0)

@pytest.fixture(scope="session")
def test_config():
    C = {
        "N": 100,
        "m": 4,
        "k": 2,
        "t": 15,
        "composition": {
            "I": 1 / 3,
            "II": 1 / 3,
            "III": 1 / 3
        }
    }
    return C

@pytest.fixture(scope="session")
def test_config2():
    C = {
        "N": 4,
        "m": 4,
        "k": 1.5,
        "t": 1,
        "composition": {
            "III": 3/4,
            "X": 1/4
        },
        "socialnorm": "Loner"
    }
    return C

@pytest.fixture(scope="session")
def test_config3():
    C1 = {
        "N": 100,
        "m": 7,
        "k": 2,
        "t": 10,
        "composition": {
            "I": 1 / 3,
            "II": 1 / 3,
            "III": 1 / 3
        }
    }

    C2 = {
        "N": 100,
        "m": 4,
        "k": 2,
        "t": 10,
        "composition": {
            "I": 1 / 3,
            "II": 1 / 3,
            "III": 1 / 4
        }
    }

    C3 = {
        "N": random.randint(-100, 0),
        "m": random.randint(-100, 0),
        "k": random.randint(-100, 0),
        "t": random.randint(-100, 0),
        "composition": {
            "I": 1 / 3,
            "II": 1 / 3,
            "III": 1 / 3
        }
    }

    C4 = {
        "N": 100,
        "m": 4,
        "k": 2,
        "t": 10,
        "composition": {
            "I": 1 / 3,
            "II": 3 / 3,
            "III": -1 / 3
        }
    }

    C5 = {
        "N": 3,
        "m": 3,
        "k": 2,
        "t": 10,
        "composition": {
            "I": 1 / 3,
            "II": 1 / 3,
            "III": 1 / 3
        }
    }

    C6 = {
        "N": 30,
        "m": 2,
        "k": 2,
        "t": 10,
        "composition": {
            "I": 1 / 3,
            "II": 1 / 3,
            "III": 1 / 3
        }
    }

    invalid_configs = [C1, C2, C3, C4, C5, C6]
    return invalid_configs
