import networkx as nx


class Examiner:
    """Namespace for running all necessary algorithms for networks within our family of models."""

    def __init__(self, network):
        self.adj = Examiner.getAdjMatrix(network)
        # Create networkx graph object to run algorithsm on
        # self.graph =
        pass

    def getClusteringCoeff(self):
        """Calculate the clustering coefficient of a network."""
        pass

    @staticmethod
    def getAdjMatrix(network):
        """Given a network, return the adjacency matrix as a numpy array."""
        return network.toNumpyArray()
