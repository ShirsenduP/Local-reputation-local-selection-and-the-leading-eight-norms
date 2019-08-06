from CodeEvolution import Network
from CodeEvolution.agent import GrGe_Agent, LrGe_Agent, LrLe_Agent
from CodeEvolution.structures import ErdosRenyi, RandomRegularLattice
from CodeEvolution.evolution import GlobalEvolution, LocalEvolution, GlobalReputation, LocalReputation


class GrGeNetwork(ErdosRenyi, GlobalReputation, GlobalEvolution, Network):
    """Erdos Renyi Network with Global Reputation and Global Evolution"""

    name = "GrGe"

    def __init__(self, _config=None):
        super().__init__(_config)
        if self.config.density != 1:
            self.config.density = 1
        self.generate(agentType=GrGe_Agent)


class LrGeNetwork(ErdosRenyi, LocalReputation, GlobalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Global Evolution (LrGe)"""

    name = "LrGe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=LrGe_Agent)


class LrLeNetwork(ErdosRenyi, LocalReputation, LocalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Local Evolution (LrLe)"""

    name = "LrLe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=LrLe_Agent)


class LrGeRRLNetwork(RandomRegularLattice, LocalReputation, GlobalEvolution, Network):
    """Random d-regular lattice with Global Reputation and Global Evolution."""

    name = "LrGeRRL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self.generate(agentType=LrGe_Agent)
