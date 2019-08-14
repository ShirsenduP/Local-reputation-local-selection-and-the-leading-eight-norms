import collections
import copy
import random
import logging

import networkx as nx
import numpy as np

from collections import deque
from matplotlib import pyplot as plt

from CodeEvolution.agent import Agent
from CodeEvolution.config import Config
from CodeEvolution.results import Results
from CodeEvolution.socialnorm import SocialNorm
from CodeEvolution.strategy import Strategy


class Network:
    """Base network class containing all the general functionality used in all models. This class should not be
    directly instantiated. """

    def __init__(self, config=Config(), agentType=Agent):
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
        logging.debug(f"Network Parameters: \t{self.__dict__}")

        # Networkx Attributes
        self.adjMatrix = None
        self.nxGraph = None
        self.modeDegree = None

    def plotGraph(self):
        arr = self.toNumpyArray()
        G = nx.from_numpy_array(arr)
        plt.subplot()
        nx.draw(G, with_labels=True)
        plt.show()

    def toNumpyArray(self):
        """Return a numpy adjacency matrix representing this network object."""

        if len(self.agentList) == 0:
            raise Exception("Network has not yet been created.")

        n = self.config.size
        adjacencyArray = np.zeros(shape=(n, n), dtype=int)

        for agent in self.agentList:
            for neighbour in agent.neighbours:
                adjacencyArray[agent.id][neighbour.id] = 1

        return adjacencyArray

    def getActualDensity(self):
        """Return the actual density of the generated network."""
        # Number of actual connections / number of potential connections

        actualConnections = 0
        for agent in self.agentList:
            # Add the number of connections of every single agent
            actualConnections += len(agent.neighbours)
        # Each connection is counted twice so divide
        actualConnections /= 2

        n = self.config.size
        potentialConnections = 0.5 * n * (n - 1)

        return actualConnections / potentialConnections

    def getSparsityParameter(self):
        """Return the minimum probability p for the G(n,p) Erdos-Renyi Random Network model for the network to be
        connected."""
        return 2 * np.log(self.config.size) / self.config.size

    def createNetwork(self, agentType):
        """Method (of some network structure) must be implemented in all sub-classes."""
        raise NotImplementedError

    def generate(self, agentType):
        """Generate a valid network."""
        # try:
        #     if self.config.density < self.getSparsityParameter():
        #         raise Exception(
        #             f"Density ({self.config.density} < {self.getSparsityParameter()}) too low for network to "
        #             f"be connected. Exiting.")
        # except TypeError as e:
        #     logging.debug("Density is set as 'None'. {}".format(e))

        Strategy.reset()
        self.createNetwork(agentType)
        # print(self)
        attempts = 0
        maxAttempts = 5
        while self.getMinDegree() < 2:

            attempts += 1
            logging.debug(f"{self.name} Network creation attempt #{attempts}/{maxAttempts}")
            # print(f"{self.name} Network creation attempt #{attempts}/{maxAttempts}")

            # Reset network
            Strategy.reset()
            self.agentList = []
            self.createNetwork(agentType)
            # print(self)

            invalidAgentCount = 0
            for agent in self.agentList:
                if len(agent.neighbours) < 2:
                    invalidAgentCount += 1
            # logging.error(f"{numberOfUnconnectedAgents} disconnected agents.")
            if invalidAgentCount > 0:
                logging.info(f"{invalidAgentCount} invalid agents.")

        if attempts == maxAttempts:
            logging.critical(f"{self.name} Network creation failed {maxAttempts} times. Exiting!")
            # raise Exception(f"{self.name} Network creation failed {maxAttempts} times. Exiting!")

    def generateConvergenceCheckpoints(self):
        """Given the configuration file for the simulation, generate a sorted list of time-steps which dictate when
        the system checks for convergence. No convergence checks occur before a quarter of the simulation has
        progressed. """
        maxPeriods = self.config.maxPeriods
        checkpoints = random.sample(range(int(maxPeriods / 4), maxPeriods), int(maxPeriods / 100))
        checkpoints.sort()
        return checkpoints

    def getMinDegree(self):
        """Return the minimum degree out of all agents within the network"""
        minDegree = np.inf
        for agent in self.agentList:
            if len(agent.neighbours) < minDegree:
                minDegree = len(agent.neighbours)
        return minDegree

    def hasMinTwoDegree(self):
        """Check if each agent on the network has a minimum of two neighbours."""
        if len(self.agentList) == 0:
            return False

        for agent in self.agentList:
            if len(agent.neighbours) < 2:
                return False
        return True

    def isConnected(self):
        if len(self.agentList) == 0:
            logging.critical("Unconnected Network")
            return False
        for agent in self.agentList:
            if len(agent.neighbours) == 0:
                logging.critical("Unconnected Network")
                return False
        return True

    def __del__(self):
        self.socialNorm = None
        self.currentPeriod = 0
        self.results = None
        self.resetTempActions()
        self.hasConverged = False
        # Strategy.reset()
        for agent in self.agentList:
            del agent.currentStrategy

    def resetTempActions(self):
        """Reset the cooperation/defection counter to zero. To be used at the end of each time-period after actions have
         been recorded."""

        for action in self.tempActions:
            self.tempActions[action] = 0

    def scanStrategies(self):
        """Update the LocalData with the proportions of all strategies at any given time."""

        # Update LocalData with census
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
            # debugNetwork = str(self)
            logging.info(f"T = {self.currentPeriod} - census: {self.getCensus()}")
            self.resetUtility()
            self.resetTempActions()
            self.runSingleTimestep()
            self.scanStrategies()
            # print(self)
            # logging.debug(self)
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

        if mainProp + mutantProp != populationSize:
            raise Exception("Initial State is unbalanced wrt to the size of the network giving non-integer numbers of "
                            "agents running a strategy.")

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

        # Get their reputations, two methods, globally available rep, or locally available rep
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

        # self.updateInteractions(agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move)
        # self.updateReputation(agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move)
        self.updateAfterSocialDilemma(agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move)

    def updateAfterSocialDilemma(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
        """Defined in GlobalReputation/LocalReputation classes."""
        raise NotImplementedError

    def resetUtility(self):
        """Reset the utility of each agent in the population. To be used at the end of every timestep."""
        for agent in self.agentList:
            agent.currentUtility = 0
        self.utilityMonitor = [{}.fromkeys(self.mainStratIDs, 0), {}.fromkeys(self.mainStratIDs, 0)]
        logging.debug(f"(t={self.currentPeriod})Network utility monitor, and agent utility trackers reset.")

    def updateInteractions(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
        """Update the local information, broadcast information about each agent's reputations to their respective
        neighbours."""

        agent1NewRep = self.socialNorm.assignReputation(agent1Reputation, agent2Reputation, agent1Move)
        agent2NewRep = self.socialNorm.assignReputation(agent2Reputation, agent1Reputation, agent2Move)

        agent1.broadcastReputation(agent1NewRep, self.config.delta)
        agent2.broadcastReputation(agent2NewRep, self.config.delta)

    def showHistory(self):
        for agent in self.agentList:
            s = f"History for agent {agent.id} \n"
            s += agent.getHistory()
            s += "\n"
            print(s)

    def checkConvergence(self):
        """Check if the system has converged. """

        if None in self.convergenceHistory:
            return

        history = [snapshot[1] for snapshot in self.convergenceHistory]
        mainID = self.mainStratIDs[0]
        epsilon = self.config.mutationProbability

        if abs(history[0][mainID] - history[1][mainID]) < 2 * epsilon and \
                abs(history[0][mainID] - history[2][mainID]) < 2 * epsilon:
            self.hasConverged = True
            self.results.convergedAt = self.currentPeriod
            logging.info(f"CONVERGENCE CHECKPOINT {self.convergenceHistory}")

    def chooseTwoAgents(self):
        agent1 = random.choice(self.agentList)
        agent2 = random.choice(self.agentList)
        # print(agent2 == agent1)
        while agent2 == agent1:
            # print(agent2 == agent1)
            agent2 = random.choice(self.agentList)
            # print(agent2)
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
        """Must be implemented through the relevant network type."""
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
        self.convergenceHistory.appendleft((self.currentPeriod, self.getCensus()))

    def getAgentWithID(self, id):
        """Return a reference to the agent object in the network with the same id # given."""
        for agent in self.agentList:
            if agent.id == id:
                return agent

    def getClusteringCoefficient(self):
        """Return the average clustering coefficient of a network."""
        try:
            coeff = nx.average_clustering(self.nxGraph)
            raise coeff
        except AttributeError:
            raise NotImplementedError("Average clustering coefficient only available for graphs generated from "
                                      "networkx with a nx.Graph object attribute.")

    def getDegreeDistribution(self):
        """Return a degree distribution of the graph as a dictionary where the keys are the range of possible
        degrees, and the values are the number of agents with that many neighbours."""

        degreeSequence = sorted([d for n, d in self.nxGraph.degree()], reverse=True)
        degreeCount = collections.Counter(degreeSequence)
        return degreeCount

    def isRegular(self):
        if self.adjMatrix is None:
            raise Exception("Lattice has not yet been initialised.")

        agentDegrees = self.adjMatrix.sum(axis=0)
        if np.any(agentDegrees != self.modeDegree):
            return False
        return True

    def plotGraph(self):
        """Using the networkx package, plot the network"""
        plt.subplot()
        nx.draw(self.nxGraph)
        plt.show()

    def __str__(self):
        s = ""
        for agent in self.agentList:
            s += str(agent) + "\n"
        return s
