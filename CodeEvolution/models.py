from CodeEvolution import Network
from CodeEvolution.agent import GrGeAgent, LrGeAgent, LrLeAgent
from CodeEvolution.structures import ErdosRenyi, RandomRegularLattice
from CodeEvolution.evolution import GlobalEvolution, LocalEvolution
from CodeEvolution.reputation import GlobalReputation, LocalReputation


class GrGeNetwork(ErdosRenyi, GlobalReputation, GlobalEvolution, Network):
    """Erdos Renyi Network with Global Reputation and Global Evolution"""

    name = "GrGe"

    def __init__(self, _config=None):
        config = _config
        config.density = 1  # Overwrite the density of any network run on GrGe to be fully connected
        super().__init__(config)
        self.generate(agentType=GrGeAgent)


class LrGeNetwork(ErdosRenyi, LocalReputation, GlobalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Global Evolution (LrGe)"""

    name = "LrGe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=LrGeAgent)


class LrLeNetwork(ErdosRenyi, LocalReputation, LocalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Local Evolution (LrLe)"""

    name = "LrLe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=LrLeAgent)


class LrGeRRLNetwork(RandomRegularLattice, LocalReputation, GlobalEvolution, Network):
    """Random d-regular lattice with Global Reputation and Global Evolution."""

    name = "LrGeRRL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=LrGeAgent)