import random

from .evolution import GlobalEvolution, LocalEvolution
from .reputation import GlobalReputation, LocalReputation
from .strategy import Strategy


class Agent:
    """Base agent class containing all the general functionality used in all models. This class should not be
    directly instantiated."""

    reputation = (0, 1)

    def __init__(self, _id, _strategy):
        self.id = _id
        self.Strategy = Strategy(_strategy)  # TODO: Refactor this so Strategy does not return an object
        self.currentReputation = random.choice(Agent.reputation)
        self.currentUtility = 0
        self.neighbours = []
        self.history = {}  # get LAST partner

    def findBestLocalStrategy(self, copyTheBest=None):
        return NotImplementedError("Must be implemented elsewhere")

    def __str__(self):
        s = f"A{self.id}(s={self.Strategy.ID}, "
        s += f"r={self.currentReputation}, "
        s += f"u={self.currentUtility}, "
        s += f"d={len(self.neighbours)})"
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


class LrLeAgent(LocalEvolution, LocalReputation, Agent):
    """Agent class implementing Local Evolution mechanisms for the Local Reputation & Local Evolution Model. This
        class should not be directly instantiated."""

    def __init__(self, _id, _strategy):
        super().__init__(_id, _strategy)


class GrLeAgent(LocalEvolution, GlobalReputation, Agent):
    """Agent class implementing Local Evolution mechanisms for the Global Reputation & Local Evolution Model. This
        class should not be directly instantiated."""

    def __init__(self, _id, _strategy):
        super().__init__(_id, _strategy)
