import logging
import random

from CodeEvolution.config import Config, State
from CodeEvolution.network import Network
from CodeEvolution.agent import Agent


class LrLe_Network(Network):
    """Network with Local Reputation and Local Evolution (LrLe)"""

    name = "LrLe"

    def __init__(self, _config):
        super().__init__(_config)
        self.name = "LrLe"
        self.generate(agentType=Agent)
        self.evolutionaryUpdateSpeed = 0.5

    def evolutionaryUpdate(self, alpha=10):
        """Local Learning - Out of the subset of agents that are connected to the focal agent, adopt the strategy of the
         best/better performing agent with some probability."""
        for agent in self.agentList:
            agent.updateStrategy(self.config.updateProbability, copyTheBest=True)

    def updateReputation(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
        """Given the agents, their reputations, and their moves, update their personal reputations (the reputation they
        use for themselves for all of their interactions)."""

        agent1PersonalReputation = self.socialNorm.assignReputation(agent1.currentReputation, agent2Reputation,
                                                                    agent1Move)
        agent2PersonalReputation = self.socialNorm.assignReputation(agent2.currentReputation, agent1Reputation,
                                                                    agent2Move)

        agent1.updatePersonalReputation(agent1PersonalReputation)
        agent2.updatePersonalReputation(agent2PersonalReputation)

    def getOpponentsReputation(self, agent1, agent2):
        """(Local reputation - return the reputations of the two randomly chosen agents. The reputation of any agent is
        accessible only to neighbours of that agent."""

        maxChecks = self.config.size
        check1 = 0
        check2 = 0

        # Choose neighbour of each agent (except the opponent of that agent)
        agent2Neighbour = random.choice(agent2.neighbours)
        agent1Neighbour = random.choice(agent1.neighbours)

        while agent2Neighbour == agent1 and check1 < maxChecks:
            agent2Neighbour = random.choice(agent2.neighbours)
            check1 += 1
        while agent1Neighbour == agent2 and check2 < maxChecks:
            agent1Neighbour = random.choice(agent1.neighbours)
            check2 += 1

        if check1 == maxChecks or check2 == maxChecks:
            logging.warning(f"{agent1.id} or {agent2.id} in this network cannot find a neighbour of his opponent that "
                            f"is not himself.")

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


if __name__ == "__main__":
    C = Config(size=2, densities=1, initialState=State(0, 1, 8))
    N = LrLe_Network(C)
    print(N.chooseTwoAgents())
