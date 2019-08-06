import logging
import random

import networkx as nx
from scipy import stats


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


class RandomRegularLattice:
    """Generate a random d-regular lattice where each node has exactly d neighbouring nodes."""

    def createNetwork(self, agentType):

        # Generate using networkx algorithms, the graph and adjacency matrix
        degree = self.config.degree
        size = self.config.size
        self.nxGraph = nx.random_regular_graph(degree, n=size)
        self.adjMatrix = nx.to_numpy_array(self.nxGraph)
        self.name = f"Regular {degree}-degree graph"
        logging.info(f"{self.name} network initialised with adjacency matrix.")

        # Create agents
        strategyDistribution = self.getStrategyCounts()
        for i in range(size):
            randomStrategyID = random.choice(strategyDistribution)
            strategyDistribution.remove(randomStrategyID)
            self.agentList.append(agentType(_id=i, _strategy=randomStrategyID))

        # Assign neighbours
        M = self.adjMatrix
        for i in range(size):
            for j in range(size):
                if int(M[i][j]) is 0:
                    continue
                else:
                    if self.agentList[j] not in self.agentList[i].neighbours:
                        self.agentList[i].neighbours.append(self.agentList[j])
                        self.agentList[j].neighbours.append(self.agentList[i])

        for agent in self.agentList:
            agent.initialiseHistory()

        agentDegrees = self.adjMatrix.sum(axis=0)
        self.modeDegree = stats.mode(agentDegrees)[0][0]