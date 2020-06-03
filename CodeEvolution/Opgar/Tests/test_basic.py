from collections import Counter

import pytest

from Opgar import opgar


def test_composition(test_config):
    dists = []
    strats = list(test_config.composition.keys())
    for i in range(100):
        P = opgar.Population(config=test_config)
        assert len(P.agents) == test_config.N

        count = Counter([agent.strategy for agent in P.agents])
        dists.append(count)

    check = {}.fromkeys(strats, 0)
    for strat in strats:
        for dist in dists:
            check[strat] += dist[strat]
        check[strat] /= 100 * test_config.N  # average population composition as a proportion of 1

    for key1, key2 in zip(check.keys(), test_config.composition.keys()):
        assert test_config.composition[key2] == pytest.approx(check[key1], rel=1e-2, abs=1e-2)


def test_public_goods_game(test_config2):
    # create population with 12 people, 4 games of public goods, 1/3 each strategy
    P = opgar.Population(config=test_config2)

    # Force everyone to be good/okay at the start
    for agent in P.agents:
        if agent.strategy == "III":
            agent.reputation = [1]
        else:
            agent.reputation = [0]

    _ = P._play_public_good_game()
    P._update_reputations()
    for agent in P.agents:
        assert agent.reputation[-1] == -1


def test_always_sums_to_one(test_config):
    P = opgar.Population(test_config)
    df = P.simulate()

    counts = df["Composition Count"]
    totals = counts.sum(axis=1)
    assert (totals == test_config.N).all()


def test_reset_agents(test_config):
    P = opgar.Population(test_config)
    P._play_public_good_game()
    P._reset_population()
    for agent in P.agents:
        assert agent.utility == 1


def test_evolve():  # TODO: test evolution function
    pass


def test_social_norm():  # TODO: test correct assignment of reputations
    pass

# TODO: Test that multiple tests run consecutively do not interfere with each other
