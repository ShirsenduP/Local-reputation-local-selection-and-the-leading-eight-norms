import logging
import random

import networkx as nx
from scipy import stats

from CodeEvolution.agent import Agent


class Structure:
    """Organisational class to house the variety of network structures that can be constructed."""

    def networkFromAdjacencyMatrix(self, agentType):
        # Create agents
        strategyDistribution = self._getListOfStrategyIDs()
        for i in range(self.config.size):
            randomStrategyID = random.choice(strategyDistribution)
            strategyDistribution.remove(randomStrategyID)
            self.agentList.append(agentType(_id=i, _strategy=randomStrategyID))

        # Assign neighbours
        M = self.adjMatrix
        for i in range(self.config.size):
            for j in range(i + 1, self.config.size):
                if int(M[i][j]) == 0:
                    continue
                else:
                    if self.agentList[j] not in self.agentList[i].neighbours:
                        self.agentList[i].neighbours.append(self.agentList[j])
                        self.agentList[j].neighbours.append(self.agentList[i])

        # Initialise each agent's record of their neighbours' reputations
        for agent in self.agentList:
            agent.history = {}.fromkeys(agent.neighbours)

        agentDegrees = self.adjMatrix.sum(axis=0)
        self.modeDegree = stats.mode(agentDegrees)[0][0]


class ErdosRenyi(Structure):
    """Generate an Erdos-Renyi Random Network with density lambda."""

    def createNetwork(self, agentType):
        """Generate an Erdos-Renyi random graph with density as specified in the configuration class (configBuilder)."""
        density = self.config.density
        size = self.config.size
        self.nxGraph = nx.fast_gnp_random_graph(size, density)
        self.adjMatrix = nx.to_numpy_array(self.nxGraph)
        self.name = f"Erdos-Renyi Random Network with density {density}"
        logging.info(f"{self.name} network initialised with adjacency matrix.")
        self.networkFromAdjacencyMatrix(agentType)


class RandomRegularLattice(Structure):
    """Generate a random d-regular lattice where each node has exactly d neighbouring nodes."""

    def createNetwork(self, agentType):
        """Attempt to create the network structure with a given strategyID distribution and config."""

        # Generate using networkx algorithms, the graph and adjacency matrix
        degree = self.config.degree
        size = self.config.size
        self.nxGraph = nx.random_regular_graph(degree, n=size)
        self.adjMatrix = nx.to_numpy_array(self.nxGraph)
        self.name = f"Regular {degree}-degree graph"
        logging.info(f"{self.name} network initialised with adjacency matrix.")
        self.networkFromAdjacencyMatrix(agentType)

    @classmethod
    def getTheoreticalDensity(cls, config):
        """Return the calculated density of a d-regular random lattice."""
        size = config.size
        d = config.degree

        # Each agent is connected to d other agents, the sum is double the total number of links
        linksInNetwork = size * d * 0.5

        # Total links possible
        linksMax = size * (size - 1) * 0.5

        return linksInNetwork / linksMax


class BarabasiAlbert(Structure):
    """Returns a random graph according to the Barabási–Albert preferential attachment model."""

    def createNetwork(self, agentType):
        """Return a Barabasi Albert network with agents using the specified configuration object."""

        # Generate using networkx algorithms, the graph and adjacency matrix
        size = self.config.size
        attachment = self.config.attachment
        self.nxGraph = nx.barabasi_albert_graph(size, attachment)
        self.adjMatrix = nx.to_numpy_array(self.nxGraph)
        self.name = f"Scale-Free Graph (Gamma = {self.config.attachment})"
        logging.info(f"{self.name} network initialised with adjacency matrix.")
        self.networkFromAdjacencyMatrix(agentType)


class WattsStrogatz(Structure):
    """Returns a random graph according to the Watts-Strogatz Small World model."""

    def createNetwork(self, agentType):
        """Using networkx algorithm, _generate a Newmann-Watts-Strogratz Small World network where n agents are
        connected in a ring topology to their k nearest neighbours with probability p."""
        k, p = self.config.smallWorld
        self.nxGraph = nx.newman_watts_strogatz_graph(self.config.size, k, p)
        self.adjMatrix = nx.to_numpy_array(self.nxGraph)
        self.name = "Newman-Watts-Strogratz Small World"
        logging.info(f"{self.name} network initialised with adjacency matrix.")
        self.networkFromAdjacencyMatrix(agentType)


class RighiCliques(Structure):
    """Implements the 4-clique structure asdadjasdjaisdajdisada."""

    def createNetwork(self, agentType):
        raise NotImplementedError
        # density = self.config.density
        # size = self.config.size
        # self.nxGraph = nx.fast_gnp_random_graph(size, density)
        # self.adjMatrix = nx.to_numpy_array(self.nxGraph)
        # self.name = f"Erdos-Renyi Random Network with density {density}"
        # logging.info(f"{self.name} network initialised with adjacency matrix.")
        # self.networkFromAdjacencyMatrix(agentType)


    def makeGraph(self, numberOfCliques):
        """Given the number of 4-cliques, _generate the graph."""

        if numberOfCliques % 2 != 0:
            raise ValueError(f'The number of cliques ({numberOfCliques} must be even.')

        def incrementCounter(counter):
            return counter+1
        numberOfAgents = 0
        def create4Clique(numberOfAgents):
            clique = []
            for i in range(4):
                clique.append(Agent(numberOfAgents+i, 0))

            return clique