import copy
import random
import logging

import networkx as nx
import numpy as np

from collections import deque
from matplotlib import pyplot as plt

from CodeEvolution.agent import Agent, GrGe_Agent, LrGe_Agent
from CodeEvolution.config import Config
from CodeEvolution.results import Results
from CodeEvolution.socialnorm import SocialNorm
from CodeEvolution.strategy import Strategy


class Network:
    """Base network class implementing all the ubiquitous simulation methods. """

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

    def plotGraph(self):
        arr = self.toNumpyArray()
        G = nx.from_numpy_array(arr)
        plt.subplot()
        nx.draw(G)
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

    def getDensity(self):
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
        """Regenerate network until """
        if self.config.density < self.getSparsityParameter():
            raise Exception(f"Density ({self.config.density} < {self.getSparsityParameter()}) too low for network to "
                            f"be connected. Exiting.")

        Strategy.reset()
        self.createNetwork(agentType)
        print(self)
        attempts = 0
        maxAttempts = 5
        while self.getMinDegree() < 2:

            attempts += 1
            # logging.error(f"{self.name} Network creation attempt #{attempts}/{maxAttempts}")
            print(f"{self.name} Network creation attempt #{attempts}/{maxAttempts}")

            # Reset network
            Strategy.reset()
            self.agentList = []
            self.createNetwork(agentType)
            print(self)

            invalidAgentCount = 0
            for agent in self.agentList:
                if len(agent.neighbours) < 2:
                    invalidAgentCount += 1
            # logging.error(f"{numberOfUnconnectedAgents} disconnected agents.")
            if invalidAgentCount > 0:
                print(f"{invalidAgentCount} invalid agents.")

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
            # debugNetwork = str(self)
            # logging.debug(f"T = {self.currentPeriod} - \ncensus: {debugNetwork}")
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


    def __str__(self):
        s = ""
        for agent in self.agentList:
            s += str(agent) + "\n"
        return s


class GlobalEvolution:
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
            # print(f"update skipped because at t = {self.currentPeriod} we have {strategyUtils.values()}")
            return

        # probability of switching to strategy i is (utility of strategy i)/(total utility of all non-negative
        # strategies)*(speed of evolution, larger the alpha, the slower the evolution)
        for strategy, _ in strategyUtils.items():
            strategyUtils[strategy] /= (totalUtil * alpha)
            # TODO What is the purpose of \alpha?

        # print(f"t = {self.currentPeriod}, probabilities are {strategyUtils}, best strategy is {bestStrategy}")

        for agent in self.agentList:
            r = random.random()
            if r < strategyUtils[bestStrategy]:
                agent.currentStrategy.changeStrategy(bestStrategy)


class LocalEvolution:
    def evolutionaryUpdate(self, alpha=10):
        """Local Learning - Out of the subset of agents that are connected to the focal agent, adopt the strategy of the
         best/better performing agent with some probability."""
        for agent in self.agentList:
            agent.updateStrategy(self.config.updateProbability, copyTheBest=True)


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


class ErdosRenyi:
    """Generate an Erdos-Renyi Random Network with density lambda."""
    def createNetwork(self, agentType):
        """Generate an Erdos-Renyi random graph with density as specified in the configuration class (configBuilder)."""

        strategyDistribution = self.getStrategyCounts()

        # Check for incorrect parameters
        if len(strategyDistribution) != self.config.size:
            agentCount = self.config.population.proportion * self.config.size
            raise Exception(f"The initial proportion of agents given running the main strategy must be such that the"
                            f" corresponding number of agents is a whole number (we cannot have {agentCount} agents!).")

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


class GrGeNetwork(ErdosRenyi, GlobalReputation, GlobalEvolution, Network):
    """Network with Global Reputation and Global Evolution"""

    name = "GrGe"

    def __init__(self, _config=None):
        super().__init__(_config)
        if self.config.density != 1:
            self.config.density = 1
        self.generate(agentType=GrGe_Agent)


class LrGeNetwork(ErdosRenyi, LocalReputation, GlobalEvolution, Network):
    """Network with Local Reputation and Global Evolution (LrGe)"""

    name = "LrGe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.name = "LrGe"
        self.generate(agentType=LrGe_Agent)


class LrLeNetwork(ErdosRenyi, LocalReputation, LocalEvolution, Network):
    """Network with Local Reputation and Local Evolution (LrLe)"""

    name = "LrLe"

    def __init__(self, _config):
        super().__init__(_config)
        self.name = "LrLe"
        self.generate(agentType=Agent)



