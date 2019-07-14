import random
import copy
import logging

from CodeEvolution.network import Network
from CodeEvolution.agent import Agent


class LrGe_Network(Network):
    """Network with Local Reputation and Global Evolution (LrGe)"""

    name = "LrGe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.createNetwork(agentType=LrGe_Agent)
        self.name = "LrGe"

    def getOpponentsReputation(self, agent1, agent2):
        """(Local reputation - return the reputations of the two randomly chosen agents. The reputation of any agent is
        accessible only to neighbours of that agent."""

        # Choose neighbour of each agent (except the opponent of that agent)
        agent2Neighbour = random.choice(agent2.neighbours)
        agent1Neighbour = random.choice(agent1.neighbours)
        while agent2Neighbour == agent1:
            agent2Neighbour = random.choice(agent2.neighbours)
        while agent1Neighbour == agent2:
            agent1Neighbour = random.choice(agent1.neighbours)

        # Calculate agents' reputations using social norm, if no history, assign random reputation
        agent2Reputation = agent2Neighbour.history[agent2]
        agent1Reputation = agent1Neighbour.history[agent1]

        # If opponent has had no previous interaction, his neighbours will not have any relevant information,
        # hence assign reputation randomly.
        if agent2Reputation is None:
            agent2Reputation = random.randint(0, 1)
        if agent1Reputation is None:
            agent1Reputation = random.randint(0, 1)

        return agent1Reputation, agent2Reputation

    def evolutionaryUpdate(self, alpha=10):
        """Global Evolution - Find the strategy with the highest utility and the proportion of the utility over the
        utilities of all strategies. COPIED FROM GrGe -> MAKE SURE ITS UP TO DATE UNTIL BETTER SOLUTION FOUND"""

        strategyUtils = copy.deepcopy(self.results.utilities[self.currentPeriod])
        logging.debug(f"(Global) Average utility: {strategyUtils}")
        # find strategy with highest utility
        bestStrategy = max(strategyUtils, key=lambda key: strategyUtils[key])

        # check for strategies with negative utility
        for strategy, utility in strategyUtils.items():
            if utility < 0:
                strategyUtils[strategy] = 0

        # if total utility is zero, no evolutionary update
        totalUtil = sum(strategyUtils.values())
        if totalUtil == 0:
            # print(f"update skipped because at t = {self.currentPeriod} we have {strategyUtils.values()}")
            return

        # probability of switching to strategy i is (utility of strategy i)/(total utility of all non-negative
        # strategies)*(speed of evolution, larger the alpha, the slower the evolution)
        for strategy, _ in strategyUtils.items():
            strategyUtils[strategy] /= (totalUtil * alpha)
            # TODO this alpha is being funny, what is its point? its arbitrary.

        # print(f"t = {self.currentPeriod}, probabilities are {strategyUtils}, best strategy is {bestStrategy}")

        for agent in self.agentList:
            r = random.random()
            if r < strategyUtils[bestStrategy]:
                agent.currentStrategy.changeStrategy(bestStrategy)
                # TODO This bit is weird, need to log this function so I can see what updates are happening and what
                #  are not happening.


class LrGe_Agent(Agent):

    def __init__(self, _id, _strategy):
        super().__init__(_id, _strategy)
        self.history = None

    def updateStrategy(self, updateProbability, copyTheBest=True):
        """Overwrite the default update strategy method which implements local learning. Strategy updates occur in the
        network.evolutionaryUpdate method."""
        pass


if __name__ == "__main__":
    pass
