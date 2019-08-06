import random
import logging

from CodeEvolution.evolution import GlobalEvolution, LocalEvolution
from CodeEvolution.strategy import Strategy


class Agent:
    """Base agent class containing all the general functionality used in all models. This class should not be
    directly instantiated. """

    reputation = (0, 1)

    def __init__(self, _id, _strategy):
        self.id = _id
        self.currentStrategy = Strategy(_strategy)
        self.currentReputation = random.choice(Agent.reputation)
        self.currentUtility = 0
        self.neighbours = []
        self.history = {}  # get LAST partner

    def updateUtility(self, payoff):
        """Update the utility or cumulative payoff of an agent."""
        self.currentUtility += payoff

    def findBestLocalStrategy(self, copyTheBest):
        """Find the strategy of your best/better performing neighbour. If there are multiple, choose randomly of the
         strategies with maximum utility."""
        neighbourUtilities = list(map(lambda x: x.currentUtility, self.neighbours))
        if copyTheBest:
            # Find the strategy locally that is performing the best
            maxLocalUtility = max(neighbourUtilities)
            indices = [i for i, x in enumerate(neighbourUtilities) if x == maxLocalUtility]
        else:
            # Find all the strategies from the neighbouring agent's who are fairing better than the focal agent
            betterLocalUtilities = [util for util in neighbourUtilities if util > self.currentUtility]
            indices = [i for i, x in enumerate(neighbourUtilities) if x == random.choice(betterLocalUtilities)]

        # Choose randomly from shortlisted agents
        bestLocalStrategyID = random.choice(indices)

        return self.neighbours[bestLocalStrategyID].currentStrategy.currentStrategyID

    def updatePersonalReputation(self, newRep):
        """Update own reputation, only to be used for an agent's own reputation from their point of view in an
        interaction."""
        self.currentReputation = newRep

    def summary(self):
        # s = "Summary of Network\n"
        s = f"Agent {self.id} is currently running strategy {self.currentStrategy} with current reputation " \
            f"{self.currentReputation}"
        return s

    def initialiseHistory(self):
        """Only keep track of interactions with your neighbours."""
        self.history = {}.fromkeys(self.neighbours)

    def recordInteraction(self, interaction):
        """Remember the previous interaction with your neighbours (and no one else)."""
        if interaction['Opponent'] in self.neighbours:
            self.history[interaction['Opponent']] = interaction

    def broadcastReputation(self, newReputation, delta):
        """Broadcast an agent's reputation following an interaction to all of his neighbours. Delta is the
        probability that a neighbour views the the agent's new reputation."""
        for agent in self.neighbours:
            r = random.random()
            if r < delta:
                agent.history[self] = newReputation
                logging.debug(f"A({self.id}) broadcast to {self.history}")

    def getHistory(self):
        """Print to the console the reputations of his neighbours from his point of view."""
        s = ""
        for neighbour in self.neighbours:
            s += f"Last interaction with neighbour {neighbour.id} was {self.history[neighbour]}\n"
        return s

    def getNeighboursUtilities(self):
        """Return a list of the utilities of every neighbour of the focal agent."""
        return [(agent.id, agent.currentStrategy.currentStrategyID, agent.currentUtility) for agent in self.neighbours]

    def updateStrategy(self, updateProbability, copyTheBest=True):
        raise NotImplementedError

    def __str__(self):
        s = "("
        s += f"Agent {self.id}, id={self.currentStrategy.currentStrategyID},"
        s += f" with neighbours {self.getNeighboursUtilities()}"
        return s


class GrGeAgent(GlobalEvolution, Agent):
    """Agent class implementing Global Evolution mechanisms for the Global Reputation & Global Evolution Model. This
    class should not be directly instantiated."""

    def __init__(self, _id, _strategy):
        super().__init__(_id, _strategy)


class LrGeAgent(GlobalEvolution, Agent):
    """Agent class implementing Global Evolution mechanisms for the Local Reputation & Global Evolution Model. This
    class should not be directly instantiated."""

    def __init__(self, _id, _strategy):
        super().__init__(_id, _strategy)


class LrLeAgent(LocalEvolution, Agent):
    """Agent class implementing Local Evolution mechanisms for the Local Reputation & Local Evolution Model. This
        class should not be directly instantiated."""

    def __int__(self, _id, _strategy):
        super().__init__(_id, _strategy)


class GrLeAgent(LocalEvolution, Agent):
    """Agent class implementing Local Evolution mechanisms for the Global Reputation & Local Evolution Model. This
        class should not be directly instantiated."""

    def __int__(self, _id, _strategy):
        super().__init__(_id, _strategy)
