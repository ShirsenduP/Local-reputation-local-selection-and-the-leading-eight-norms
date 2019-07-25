import collections
import logging

from scipy import stats
import numpy as np

from CodeEvolution.network import Network
from CodeEvolution.agent import Agent
from CodeEvolution.config import Config, State

from oct2py import Oct2Py
import networkx as nx
from matplotlib import pyplot as plt


class RegularLattice(Network):
    """Create and run simulations with various types of regular lattices."""

    def __init__(self, _config=Config()):
        super().__init__(_config)
        self.name = None
        self.adjMatrix = None
        self.nxGraph = None
        self.modeDegree = None
        logging.warn("Ignoring density value in config object for regular lattice!")

    def getDegreeDistribution(self):
        """Return a degree distribution of the graph as a dictionary where the keys are the range of possible
        degrees, and the values are the number of agents with that many neighbours."""

        degreeSequence = sorted([d for n, d in self.nxGraph.degree()], reverse=True)
        degreeCount = collections.Counter(degreeSequence)
        return degreeCount

    def makeNwsSmallWorld(self, k, p=0):
        """Using networkx algorithm, generate a Newmann-Watts-Strogratz Small World network where n agents are
        connected in a ring topology to their k nearest neighbours with probability p."""
        self.nxGraph = nx.newman_watts_strogatz_graph(self.config.size, k, p)
        self.adjMatrix = nx.to_numpy_array(self.nxGraph)
        self.name = "Newmann-Watts-Strogratz Small World"
        logging.info(f"{self.name} network initialised with adjacency matrix.")

    def makeRegular(self, degree):
        """Using the networkx algorithms, get the adjacency matrix for a d-regular random graph."""
        self.nxGraph = nx.random_regular_graph(degree, n=self.config.size)
        self.adjMatrix = nx.to_numpy_array(self.nxGraph)
        self.name = f"Regular {degree}-degree graph"
        logging.info(f"{self.name} network initialised with adjacency matrix.")

    def makeCliqueLattice(self):
        """Agents are created in cliques of 4 where each agent here is connected with each other agent in the clique.
        Then each agent in the clique is connected to a single agent from another distinct clique. For diagram of
        network, see S12 in supplementary documents from Righi S., Takacs K. (2018).

            Righi S., Takacs K. (2018) "Social Closure and the Evolution of
            Cooperation via Indirect Reciprocity", Scientific Reports
            https://github.com/simonerighi/RighiTakacs_ScientificReports2018
        """

        oc = Oct2Py()
        self.adjMatrix = oc.lattice_structure(self.config.size)
        self.name = "Regular Clique Lattice"
        self.nxGraph = nx.from_numpy_array(self.adjMatrix)
        logging.info(f"{self.name} network initialised with adjacency matrix.")

    def makeLattice(self, dimensions=[2, 3, 4]):
        """Using the networkx algorithms, get the adjacency matrix for a grid network found at:
        https://networkx.github.io/documentation/latest/reference/generated/networkx.generators.lattice.grid_graph.html
        """
        self.nxGraph = nx.grid_graph(dimensions)
        self.adjMatrix = nx.to_numpy_array(self.nxGraph)
        self.name = "Regular Grid Lattice"
        logging.info(f"{self.name} network initialised with adjacency matrix.")

    def make2DLattice(self, dimensions=(2, 3)):
        """Using the networkx algorithms, get the adjacency matrix for a 2d grid network found at:
        https://networkx.github.io/documentation/
            latest/reference/generated/networkx.generators.lattice.grid_2d_graph.html"""
        m, n = dimensions
        self.nxGraph = nx.grid_2d_graph(m, n)
        self.adjMatrix = nx.to_numpy_array(self.nxGraph)
        self.name = "Regular 2D Grid Lattice"
        logging.info(f"{self.name} network initialised with adjacency matrix.")

    def makeHexLattice(self, dimensions=(2, 3)):
        """Using the networkx algorithms, get the adjacency matrix for a hexagonal grid network found at:
        https://networkx.github.io/documentation/
        latest/reference/generated/networkx.generators.lattice.hexagonal_lattice_graph.html"""
        m, n = dimensions
        self.nxGraph = nx.hexagonal_lattice_graph(m, n)
        self.adjMatrix = nx.to_numpy_array(self.nxGraph)
        self.name = "Regular Hexagonal Grid Lattice"
        logging.info(f"{self.name} network initialised with adjacency matrix.")

    def createNetwork(self, agentType=Agent):
        """Using a generated adjacency matrix, generate the custom network with custom agents."""

        if self.adjMatrix is None:
            raise Exception("Adjacency Matrix has not yet been created.")
        if self.config.population.proportion is not 1:
            raise NotImplementedError("Cannot alter the starting proportion yet! Consider only an initial population "
                                      "running a single strategy only!")
        M = self.adjMatrix
        index1, index2 = M.shape

        # Create all the agents
        for i in range(index1):
            self.agentList.append(agentType(_id=i, _strategy=self.config.population.ID))

        for i in range(index1):
            for j in range(index2):
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

    def plotGraph(self):
        """Using the networkx package, plot the network"""
        plt.subplot()
        nx.draw(self.nxGraph)
        plt.show()

    def isRegular(self):
        if self.adjMatrix is None:
            raise Exception("Lattice has not yet been initialised.")

        agentDegrees = self.adjMatrix.sum(axis=0)
        if np.any(agentDegrees != self.modeDegree):
            return False
        return True


if __name__ == "__main__":
    C = Config(size=24, initialState=State(0, 1, 8), densities=None)
    N = RegularLattice(C)
    N.makeNwsSmallWorld(k=4)
    N.createNetwork()
    # print(N.isRegular())
    N.plotGraph()
    # print(N.getDegreeDistribution())
    print(N)
