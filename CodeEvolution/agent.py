import random
import logging

from CodeEvolution.reputation import GlobalReputation, LocalReputation
from CodeEvolution.evolution import GlobalEvolution, LocalEvolution
from CodeEvolution.strategy import Strategy


class Agent:
    """Base agent class containing all the general functionality used in all models. This class should not be
    directly instantiated."""

    reputation = (0, 1)

    def __init__(self, _id, _strategy):
        self.id = _id
        self.Strategy = Strategy(_strategy)
        self.currentReputation = random.choice(Agent.reputation)
        self.currentUtility = 0
        self.neighbours = []

    def findBestLocalStrategy(self, copyTheBest=None):
        """Find the strategy of your best/better performing neighbour. If there are multiple, choose randomly of the
         strategies with maximum utility."""
        neighbourUtilities = list(
            map(lambda x: x.currentUtility, self.neighbours))
        if copyTheBest:
            # Find the strategy locally that is performing the best
            maxLocalUtility = max(neighbourUtilities)
            indices = [i for i, x in enumerate(
                neighbourUtilities) if x == maxLocalUtility]
        else:
            # Find all the strategies from the neighbouring agent's who are fairing better than the focal agent
            betterLocalUtilities = [
                util for util in neighbourUtilities if util > self.currentUtility]
            indices = [i for i, x in enumerate(
                neighbourUtilities) if x == random.choice(betterLocalUtilities)]

        # Choose randomly from shortlisted agents
        bestLocalStrategyID = random.choice(indices)

        return self.neighbours[bestLocalStrategyID].Strategy.ID

    def getNeighboursUtilities(self):
        """Return a list of the utilities of every neighbour of the focal agent."""
        return [(agent.id, agent.Strategy.ID, agent.currentUtility) for agent in self.neighbours]

    def __del__(self):
        del self.id
        self.Strategy = None
        del self.currentReputation
        del self.currentUtility
        del self.neighbours

    def __str__(self):
        s = f"Agent {self.id}, strategy={self.Strategy.ID},"
        s += f" with {len(self.neighbours)} neighbours"
        return s


class GrGeAgent(GlobalEvolution, GlobalReputation, Agent):
    """Agent class implementing Global Evolution mechanisms for the Global Reputation & Global Evolution Model. This
    class should not be directly instantiated."""

    def __init__(self, _id, _strategy):
        super().__init__(_id, _strategy)


class LrGeAgent(GlobalEvolution, LocalReputation, Agent):
    """Agent class implementing Global Evolution mechanisms for the Local Reputation & Global Evolution Model. This
    class should not be directly instantiated."""

    def __init__(self, _id, _strategy):
        super().__init__(_id, _strategy)
        self.history = {}  # get LAST partner


class LrLeAgent(LocalEvolution, LocalReputation, Agent):
    """Agent class implementing Local Evolution mechanisms for the Local Reputation & Local Evolution Model. This
        class should not be directly instantiated."""

    def __init__(self, _id, _strategy):
        super().__init__(_id, _strategy)
        self.history = {}  # get LAST partner


class GrLeAgent(LocalEvolution, GlobalReputation, Agent):
    """Agent class implementing Local Evolution mechanisms for the Global Reputation & Local Evolution Model. This
        class should not be directly instantiated."""

    def __init__(self, _id, _strategy):
        super().__init__(_id, _strategy)

