import logging
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

    def updateAfterSocialDilemma(self, agent1, agent2, agent1OldRep, agent2OldRep, agent1Move, agent2Move):
        """(Global Reputation) This method calculates and updates the respective personal reputations of each agent
        given their previous reputations and their moves.

        NOTE:
        The reputations here 'agent1OldRep' and 'agent2OldRep are given within Network.playSocialDilemma: the
        Network.getOpponentsReputations line defined in the Global Reputation class. These two reputations are directly
        the reputations seen by the agents themselves and everyone in the population."""
        pass


class LocalReputation:
    def getOpponentsReputation(self, agent1, agent2):
        """(Local reputation - return the reputations of the two randomly chosen agents. The reputation of any agent is
        accessible only to neighbours of that agent."""

        # Choose neighbour of each agent (except each other if they are neighbours)
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

        # agent1.updatePersonalReputation(agent1PersonalReputation)
        # agent2.updatePersonalReputation(agent2PersonalReputation)
        agent1.currentReputation = agent1PersonalReputation
        agent2.currentReputation = agent2PersonalReputation

    def updateAfterSocialDilemma(self, agent1, agent2, agent1OldRep, agent2OldRep, agent1Move, agent2Move):
        """(Local Reputation) This method calculates and updates the neighbours of an agent with his new reputation.

        NOTE:
        The reputations here 'agent1OldRep' and 'agent2OldRep are given within Network.playSocialDilemma: the
        Network.getOpponentsReputations line assigned by the Local Reputation class.

        From agent1's POV, he knows his personal reputation (agent1.currentReputation), and his opponent's reputation
        through his neighbour (agent2OldRep), therefore his new reputation for himself and all of his neighbours is
        calculated with these values.
history
        From agent2's POV, he knows his personal rep(agent2.currentReputation) and his neighbours (agent1OldRep).
        This is what his new reputation will be based on, saved for his own knowledge and sent to his neighbours."""

        agent1NewRep = self.socialNorm.assignReputation(agent1.currentReputation, agent2OldRep, agent1Move)
        agent2NewRep = self.socialNorm.assignReputation(agent2.currentReputation, agent1OldRep, agent2Move)

        # agent1.updatePersonalReputation(agent1NewRep)
        # agent2.updatePersonalReputation(agent2NewRep)
        agent1.currentReputation = agent1NewRep
        agent2.currentReputation = agent2NewRep

        agent1.broadcastReputation(agent1NewRep, self.config.delta)
        agent2.broadcastReputation(agent2NewRep, self.config.delta)
