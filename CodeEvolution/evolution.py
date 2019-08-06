import copy
import logging
import random


class GlobalEvolution:
    """This class supplies the global evolutionary mechanisms to any subclass that inherits from it. This class should
    not be directly instantiated."""

    def evolutionaryUpdate(self, alpha=10):
        """Global Evolution - Find the strategy with the highest utility and the proportion of the utility over the
         utilities of all strategies."""

        strategyUtils = copy.deepcopy(self.results.utilities[self.currentPeriod])

        # find strategy with highest utility
        bestStrategy = max(strategyUtils, key=lambda key: strategyUtils[key])

        # check for strategies with negative utility
        for strategy, utility in strategyUtils.items():
            if utility < 0:
                strategyUtils[strategy] = 0

        # if total utility is zero, no evolutionary update
        totalUtil = sum(strategyUtils.values())
        if totalUtil == 0:
            logging.debug(f"update skipped because at t = {self.currentPeriod} we have {strategyUtils.values()}")
            return

        # probability of switching to strategy i is (utility of strategy i)/(total utility of all non-negative
        # strategies)*(speed of evolution, larger the alpha, the slower the evolution)
        for strategy, _ in strategyUtils.items():
            strategyUtils[strategy] /= (totalUtil * alpha)
            # TODO What is the purpose of \alpha?

        logging.debug(f"t = {self.currentPeriod}, probabilities are {strategyUtils}, best strategy is {bestStrategy}")

        for agent in self.agentList:
            r = random.random()
            if r < strategyUtils[bestStrategy]:
                agent.currentStrategy.changeStrategy(bestStrategy)

    def updateStrategy(self, updateProbability, copyTheBest=True):
        """Overwrite the default update strategy method which implements local learning. Strategy updates occur in the
         network.evolutionaryUpdate method."""
        pass


class LocalEvolution:
    """This class supplies the local evolutionary mechanisms to any subclass that inherits from it. This class should
    not be directly instantiated."""

    def evolutionaryUpdate(self, alpha=10):
        """Local Learning - Out of the subset of agents that are connected to the focal agent, adopt the strategy of the
         best/better performing agent with some probability."""
        for agent in self.agentList:
            agent.updateStrategy(self.config.updateProbability, copyTheBest=True)

    def updateStrategy(self, updateProbability, copyTheBest=True):
        """Local Evolution - Switch strategies to the strategy used by the best performing neighbour of
        the agent with some probability."""
        # TODO Implement copyTheBetter strategyUpdate
        r = random.random()
        if r < updateProbability:
            newStrategyID = self.findBestLocalStrategy(copyTheBest)
            if newStrategyID == self.currentStrategy.currentStrategyID:
                return
            self.currentStrategy.changeStrategy(newStrategyID)


class GlobalReputation:
    def getOpponentsReputation(self, agent1, agent2):
        """(Global reputation - return the reputations of the two randomly chosen agents. The reputation of any agent
        is accessible to every other agent in the population."""
        return agent1.currentReputation, agent2.currentReputation

    def updateReputation(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
        """Assign reputations following an interaction with each agent's globally known reputation and not the
        calculated reputation as default."""

        agent1NewReputation = self.socialNorm.assignReputation(agent1.currentReputation, agent2.currentReputation,
                                                               agent1Move)
        agent2NewReputation = self.socialNorm.assignReputation(agent2.currentReputation, agent1.currentReputation,
                                                               agent2Move)

        agent1.updatePersonalReputation(agent1NewReputation)
        agent2.updatePersonalReputation(agent2NewReputation)


class LocalReputation:
    def getOpponentsReputation(self, agent1, agent2):
        """(Local reputation - return the reputations of the two randomly chosen agents. The reputation of any agent is
        accessible only to neighbours of that agent."""

        # Choose neighbour of each agent (except the opponent of that agent)
        agent2Neighbours = [agent.id for agent in agent2.neighbours]
        agent1Neighbours = [agent.id for agent in agent1.neighbours]

        if agent2.id in agent1Neighbours:
            logging.debug("before: {}".format(agent1Neighbours))
            agent1Neighbours.remove(agent2.id)
            logging.debug("after: {}".format(agent1Neighbours))
        if agent1.id in agent2Neighbours:
            logging.debug("before: {}".format(agent2Neighbours))
            agent2Neighbours.remove(agent1.id)
            logging.debug("after: {}".format(agent2Neighbours))

        agent2NeighbourID = random.choice(agent2Neighbours)
        agent1NeighbourID = random.choice(agent1Neighbours)

        agent2Neighbour = self.getAgentWithID(agent2NeighbourID)
        agent1Neighbour = self.getAgentWithID(agent1NeighbourID)

        if agent2Neighbour == agent1 or agent1Neighbour == agent2:
            logging.critical(f"An agent is considering himself as a neighbour of his opponent. This is NOT ALLOWED!")

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

    def updateReputation(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
        """Given the agents, their reputations, and their moves, update their personal reputations (the reputation they
        use for themselves for all of their interactions)."""

        agent1PersonalReputation = self.socialNorm.assignReputation(agent1.currentReputation, agent2Reputation,
                                                                    agent1Move)
        agent2PersonalReputation = self.socialNorm.assignReputation(agent2.currentReputation, agent1Reputation,
                                                                    agent2Move)

        agent1.updatePersonalReputation(agent1PersonalReputation)
        agent2.updatePersonalReputation(agent2PersonalReputation)