import copy
import random

from collections import deque

from CodeEvolution.agent import Agent
from CodeEvolution.results import Results
from CodeEvolution.socialnorm import SocialNorm
from CodeEvolution.strategy import Strategy


class Network:

    def __init__(self, config, agentType=Agent):
        self.config = config
        self.name = "Network"
        self.mainStratIDs = (config.population.ID, config.mutant.ID)
        self.agentList = []
        self.socialNorm = SocialNorm(config.socialNormID)
        self.results = Results(config)
        self.tempActions = {'C': 0, 'D': 0}
        self.utilityMonitor = [{}.fromkeys(self.mainStratIDs, 0), {}.fromkeys(self.mainStratIDs, 0)]  # index0 captures
        # #OfInteractions of an agent with some strategy, index1 captures the total cumulative payoff of all agents
        # running that strategy
        self.currentPeriod = 0
        self.convergenceCheckIntervals = self.generateConvergenceCheckpoints()
        self.convergenceHistory = deque(3 * [None], 3)
        self.hasConverged = False
        self.dilemma = config.socialDilemma

    def generateConvergenceCheckpoints(self):
        """Given the configuration file for the simulation, generate a sorted list of time-steps which dictate when
        the system checks for convergence. No convergence checks occur before a quarter of the simulation has
        progressed. """
        maxPeriods = self.config.maxPeriods
        checkpoints = random.sample(range(int(maxPeriods / 4), maxPeriods), int(maxPeriods / 100))
        checkpoints.sort()
        return checkpoints

    def isConnected(self):
        isConnected = True
        for agent in self.agentList:
            if len(agent.neighbours) == 0:
                isConnected = False
        return isConnected

    def __del__(self):
        self.socialNorm = None
        self.currentPeriod = 0
        self.results = None
        self.resetTempActions()
        self.hasConverged = False
        Strategy.reset()

    def resetTempActions(self):
        """Reset the cooperation/defection counter to zero. To be used at the end of each time-period after actions have
         been recorded."""

        for action in self.tempActions:
            self.tempActions[action] = 0

    def scanStrategies(self):
        """Update the results with the proportions of all strategies at any given time."""

        # Update results with census
        census = self.getCensus(proportions=True)
        self.results.strategyProportions[self.currentPeriod] = census

        interactionsDict = self.utilityMonitor[0]
        payoffDict = self.utilityMonitor[1]
        averageUtilities = {}.fromkeys(self.mainStratIDs, 0)

        for key, _ in averageUtilities.items():
            if interactionsDict[key]:
                averageUtilities[key] = payoffDict[key] / interactionsDict[key]
        self.results.utilities[self.currentPeriod] = averageUtilities

    def runSimulation(self):
        """Run full simulation for upto total number of simulations defined in the config object' or up until the
        system converges at pre-allocated randomly chosen convergence check intervals."""
        self.scanStrategies()
        while self.currentPeriod < self.config.maxPeriods and not self.hasConverged:
            self.resetUtility()
            self.resetTempActions()
            self.runSingleTimestep()
            self.scanStrategies()
            # print(self)
            self.evolutionaryUpdate()
            self.mutation(self.config.mutant.ID)
            if self.currentPeriod in self.convergenceCheckIntervals:
                self.grabSnapshot()
                self.checkConvergence()

            if self.hasConverged or self.currentPeriod == self.config.maxPeriods - 1:
                self.results.convergedAt = self.currentPeriod
                break
            else:
                self.currentPeriod += 1

    def getStrategyCounts(self):
        """Return a list where each element represents the strategyID of an agent."""

        populationSize = self.config.size
        mainID = self.config.population.ID
        mutantID = self.config.mutant.ID
        mainProp = int(self.config.population.proportion * populationSize)
        mutantProp = int(self.config.mutant.proportion * populationSize)

        mainPop = [mainID] * mainProp
        mutantPop = [mutantID] * mutantProp
        return mainPop + mutantPop

    def getCensus(self, proportions=False):
        """Return a dictionary where the key-value pairs are the strategy IDs and the number of agents running that
        strategy. Optionally return the proportions of strategies run by the agents in the population instead."""

        censusCopy = copy.deepcopy(Strategy.census)
        if not proportions:
            return censusCopy
        else:
            size = self.config.size
            for key, _ in censusCopy.items():
                censusCopy[key] /= size
            return censusCopy

    def createNetwork(self, agentType):
        """Generate an Erdos-Renyi random graph with density as specified in the configuration class (configBuilder)."""

        strategyDistribution = self.getStrategyCounts()

        for agentID in range(self.config.size):
            randomIDIndex = random.randint(0, len(strategyDistribution) - 1)
            self.agentList.append(agentType(_id=agentID, _strategy=strategyDistribution[randomIDIndex]))
            strategyDistribution.pop(randomIDIndex)

        for agentID1 in range(self.config.size):
            for agentID2 in range(agentID1 + 1, self.config.size):
                if agentID1 != agentID2:
                    r = random.random()
                    if r < self.config.density:
                        if self.agentList[agentID2] not in self.agentList[agentID1].neighbours:
                            self.agentList[agentID1].neighbours.append(self.agentList[agentID2])
                        if self.agentList[agentID1] not in self.agentList[agentID2].neighbours:
                            self.agentList[agentID2].neighbours.append(self.agentList[agentID1])

        for agent in self.agentList:
            agent.initialiseHistory()

    def getOpponentsReputation(self, agent1, agent2):
        """Must be implemented through the relevant network type. Can be Global or Local."""
        raise NotImplementedError

    def updateMonitor(self, agent1, agent2, payoff1, payoff2):
        """Track the utilities of each strategy as well as the number of interactions undertaken by an agent running
        a strategy."""
        agent1ID = agent1.currentStrategy.currentStrategyID
        agent2ID = agent2.currentStrategy.currentStrategyID
        self.utilityMonitor[0][agent1ID] += 1
        self.utilityMonitor[1][agent1ID] += payoff1
        self.utilityMonitor[0][agent2ID] += 1
        self.utilityMonitor[1][agent2ID] += payoff2

    def playSocialDilemma(self):

        # Two agents chosen randomly from the population
        agent1, agent2 = self.chooseTwoAgents()
        agent1Reputation, agent2Reputation = self.getOpponentsReputation(agent1, agent2)

        # Each agent calculates their move according to their behavioural strategy
        agent1Move = agent1.currentStrategy.chooseAction(agent1.currentReputation, agent2Reputation)
        agent2Move = agent2.currentStrategy.chooseAction(agent2.currentReputation, agent1Reputation)
        self.tempActions[agent1Move] += 1
        self.tempActions[agent2Move] += 1

        # Calculate each agent's payoff
        payoff1, payoff2 = self.dilemma.playGame(agent1Move, agent2Move)
        self.updateMonitor(agent1, agent2, payoff1, payoff2)

        # Update agents personal utilities for (LOCAL) evolutionary update
        agent1.updateUtility(payoff1)
        agent2.updateUtility(payoff2)

        self.updateInteractions(agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move)
        self.updateReputation(agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move)

    def resetUtility(self):
        """Reset the utility of each agent in the population. To be used at the end of every timestep."""
        for agent in self.agentList:
            agent.currentUtility = 0
        self.utilityMonitor = [{}.fromkeys(self.mainStratIDs, 0), {}.fromkeys(self.mainStratIDs, 0)]

    def updateInteractions(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
        interaction12 = {
            'Opponent'           : agent2,
            'Focal Reputation'   : agent1.currentReputation,
            'Opponent Reputation': agent2Reputation,
            'Focal Move'         : agent1Move,
            'Opponent Move'      : agent2Move
        }
        agent1.recordInteraction(interaction12)
        interaction21 = {
            'Opponent'           : agent1,
            'Focal Reputation'   : agent2.currentReputation,
            'Opponent Reputation': agent1Reputation,
            'Focal Move'         : agent2Move,
            'Opponent Move'      : agent1Move
        }
        agent2.recordInteraction(interaction21)

    def updateReputation(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
        """Assign reputations following an interaction with each agent's globally known reputation and not the
        calculated reputation as default."""

        agent1NewReputation = self.socialNorm.assignReputation(agent1.currentReputation, agent2.currentReputation,
                                                               agent1Move)
        agent2NewReputation = self.socialNorm.assignReputation(agent2.currentReputation, agent1.currentReputation,
                                                               agent2Move)

        agent1.updatePersonalReputation(agent1NewReputation)
        agent2.updatePersonalReputation(agent2NewReputation)
        # TODO Whats the point of agent1Reputation and agent2Reputation if its being newly calculated within the method? Check whats going on here

    def showHistory(self):
        for agent in self.agentList:
            s = f"History for agent {agent.id} \n"
            s += agent.getHistory()
            s += "\n"
            print(s)

    def checkConvergence(self):
        """Check if the network has converged or not by checking the last 3 snapshots taken at randomly chosen
        intervals."""

        history = self.convergenceHistory

        # Minimum 3 snapshots needed to check for convergence (as defined in self.convergenceHistory)
        if None in history:
            return

        if history[2] == history[1] and history[1] == history[0]:
            print(f"HAS CONVERGED AT {history}, checks at {self.convergenceCheckIntervals}")
            self.hasConverged = True
            self.results.convergedAt = self.currentPeriod

    def chooseTwoAgents(self):
        agent1 = random.choice(self.agentList)
        agent2 = random.choice(self.agentList)
        while agent2 == agent1:
            agent2 = random.choice(self.agentList)
        return agent1, agent2

    def mutation(self, mutantStrategyID):
        """Each agent has probability of (alpha/n) of becoming a mutant in any time period where alpha is the
        expected number of mutants added per time-step."""
        probabilityOfMutation = self.config.mutationProbability / self.config.size
        for agent in self.agentList:
            r = random.random()
            if r < probabilityOfMutation:
                # print(f"agent {agent.id} mutation, {agent.currentStrategy.currentStrategyID} to {mutantStrategyID}")
                agent.currentStrategy.changeStrategy(mutantStrategyID)
                if self.currentPeriod not in self.results.mutantTracker.keys():
                    self.results.mutantTracker[self.currentPeriod] = 1
                else:
                    self.results.mutantTracker[self.currentPeriod] += 1

        # If no mutants added, append 0 to mutantTracker
        if self.currentPeriod not in self.results.mutantTracker.keys():
            self.results.mutantTracker[self.currentPeriod] = 0

    def evolutionaryUpdate(self, alpha=10):
        """Must be implemented through the relevent network type."""
        raise NotImplementedError

    def runSingleTimestep(self):
        """Run one single time-step with multiple interactions between randomly selected agents"""
        self.playSocialDilemma()
        r = random.random()
        while r < self.config.omega:
            self.playSocialDilemma()
            r = random.random()

        self.results.updateActions(self.tempActions)

    def grabSnapshot(self):
        self.convergenceHistory.appendleft(self.getCensus())

    def __str__(self):
        s = ""
        for agent in self.agentList:
            s += str(agent) + "\n"
        return s


if __name__ == "__main__":
    pass
