from CodeEvolution.network import Network
from CodeEvolution.agent import GrGeAgent, LrGeAgent, LrLeAgent, GrLeAgent
from CodeEvolution.structures import ErdosRenyi, RandomRegularLattice, BarabasiAlbert, WattsStrogatz
from CodeEvolution.evolution import GlobalEvolution, LocalEvolution
from CodeEvolution.reputation import GlobalReputation, LocalReputation


class GrGeERNetwork(ErdosRenyi, GlobalReputation, GlobalEvolution, Network):
    """Erdos Renyi Network with Global Reputation and Global Evolution"""

    name = "GrGe"

    def __init__(self, _config=None):
        config = _config
        config.density = 1  # Overwrite the density of any network run on GrGe to be fully connected
        super().__init__(config)
        self.generate(agentType=GrGeAgent)


class LrGeERNetwork(ErdosRenyi, LocalReputation, GlobalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Global Evolution (LrGe)"""

    name = "LrGe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=LrGeAgent)


class LrLeERNetwork(ErdosRenyi, LocalReputation, LocalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Local Evolution (LrLe)"""

    name = "LrLe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=LrLeAgent)


class GrLeERNetwork(ErdosRenyi, GlobalReputation, LocalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Global Evolution (GrLe)"""

    name = "GrLe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=GrLeAgent)

class LrGeRRLNetwork(RandomRegularLattice, LocalReputation, GlobalEvolution, Network):
    """Random d-regular lattice with Global Reputation and Global Evolution."""

    name = "LrGeRRL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=LrGeAgent)


class LrGePLNetwork(BarabasiAlbert, LocalReputation, GlobalEvolution, Network):
    """Scale-free network generated using a power law distribution."""

    name = "LrGePL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=LrGeAgent)


class LrGeWSSWNetwork(WattsStrogatz, LocalReputation, GlobalEvolution, Network):
    """Watts-Strogatz Small World model with Local Reputation and Global Evolution."""

    name = "LrGeWSSW"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=LrGeAgent)
