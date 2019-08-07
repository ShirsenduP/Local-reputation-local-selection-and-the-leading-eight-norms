import logging

from CodeEvolution.network import Network
from CodeEvolution.config import Config, State

import networkx as nx


class Lattice(Network):
    """Create and run simulations with various types of regular lattices."""

    def __init__(self, _config=Config()):
        super(Network).__init__(_config)
        self.name = None
        self.adjMatrix = None
        self.nxGraph = None
        self.modeDegree = None
        logging.warn("Ignoring density value in config object for regular lattice!")

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


'''
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
        logging.info(f"{self.name} network initialised with adjacency matrix.")'''
