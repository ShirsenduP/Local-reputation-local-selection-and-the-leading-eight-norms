import random


class GlobalReputation:

    def getOpponentsReputation(self, agent1, agent2):
        """(Global reputation - return the reputations of the two randomly chosen agents. The reputation of any agent
        is accessible to every other agent in the population."""
        return agent1.currentReputation, agent2.currentReputation

    def updateReputation(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
        """Assign reputations following an interaction with each agent's globally known reputation and not the
        calculated reputation as default."""

        agent1NewReputation = self.socialNorm.assignReputation(
            agent1Reputation,
            agent2Reputation,
            agent1Move
        )
        agent2NewReputation = self.socialNorm.assignReputation(
            agent2Reputation,
            agent1Reputation,
            agent2Move
        )

        agent1.currentReputation = agent1NewReputation
        agent2.currentReputation = agent2NewReputation


class LocalReputation:

    def getOpponentsReputation(self, agent1, agent2):
        """(Local reputation - return the reputations of the two randomly chosen agents. The reputation of any agent is
        accessible only to neighbours of that agent."""

        agent1Neighbour = random.choice(agent1.neighbours)
        agent2Neighbour = random.choice(agent2.neighbours)

        while agent2Neighbour is agent1:
            agent2Neighbour = random.choice(agent2.neighbours)
        while agent1Neighbour is agent2:
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

    def updateReputation(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
        """Given the agents, their reputations, and their moves, update their personal reputations (the reputation they
        use for themselves for all of their interactions)."""

        agent1PersonalReputation = self.socialNorm.assignReputation(
            agent1Reputation,
            agent2Reputation,
            agent1Move
        )
        agent2PersonalReputation = self.socialNorm.assignReputation(
            agent2Reputation,
            agent1Reputation,
            agent2Move
        )

        # Broadcast each agent's new reputation to their neighbours with probability delta
        for nbr in agent1.neighbours:
            if random.random() < self.config.delta:
                nbr.history[agent1] = agent1PersonalReputation
        for nbr in agent2.neighbours:
            if random.random() < self.config.delta:
                nbr.history[agent2] = agent2PersonalReputation
