import logging

from .agent import GrGeAgent, LrGeAgent, LrLeAgent, GrLeAgent
from .evolution import GlobalEvolution, LocalEvolution
from .network import Network
from .reputation import GlobalReputation, LocalReputation
from .structures import ErdosRenyi, RandomRegularLattice, BarabasiAlbert, WattsStrogatz


#############################
## Erdos Renyi Random Network
#############################

class GrGeERNetwork(ErdosRenyi, GlobalReputation, GlobalEvolution, Network):
    """Erdos Renyi Network with Global Reputation and Global Evolution"""

    name = "GrGe"

    def __init__(self, _config=None):
        config = _config
        if config.density != 1:
            logging.warning(f'Changing GrGeER Network density from {config.density} to 1')
            config.density = 1  # Overwrite the density of any network run on GrGe to be fully connected
        if config.delta != 1:
            config.delta = 1
            logging.warning("Delta (probability of successful reputation broadcast) is not 1, there will be errors!")
        super().__init__(config)
        self._generate(agentType=GrGeAgent)


class LrGeERNetwork(ErdosRenyi, LocalReputation, GlobalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Global Evolution (LrGe)"""

    name = "LrGe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=LrGeAgent)


class LrLeERNetwork(ErdosRenyi, LocalReputation, LocalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Local Evolution (LrLe)"""

    name = "LrLe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=LrLeAgent)


class GrLeERNetwork(ErdosRenyi, GlobalReputation, LocalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Global Evolution (GrLe)"""

    name = "GrLe"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=GrLeAgent)


#############################
## D REGULAR LATTICE
#############################

class GrGeRRLNetwork(RandomRegularLattice, GlobalReputation, GlobalEvolution, Network):
    """Random d-regular lattice with global reputation and global evolution on a d-regular random lattice."""

    name = "GrGeRRL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=GrGeAgent)


class LrGeRRLNetwork(RandomRegularLattice, LocalReputation, GlobalEvolution, Network):
    """Random d-regular lattice with Local Reputation and Global Evolution on a d-regular random lattice."""

    name = "LrGeRRL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=LrGeAgent)


class LrLeRRLNetwork(RandomRegularLattice, LocalReputation, LocalEvolution, Network):
    """Random d-regular lattice with Local Reputation and Local Evolution on a d-regular random lattice."""

    name = "LrLeRRL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=LrLeAgent)


class GrLeRRLNetwork(RandomRegularLattice, GlobalReputation, LocalEvolution, Network):
    """Random d-regular lattice with Global Reputation and Local Evolution on a d-regular random lattice."""

    name = "GrLeRRL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=GrLeAgent)


#############################
## POWER LAW NETWORK
#############################

class GrGePLNetwork(BarabasiAlbert, GlobalReputation, GlobalEvolution, Network):
    """Scale-free network generated using a power law distribution with global reputation and global evolution."""

    name = "GrGePL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=GrGeAgent)


class LrGePLNetwork(BarabasiAlbert, LocalReputation, GlobalEvolution, Network):
    """Scale-free network generated using a power law distribution with local reputation and global evolution."""

    name = "LrGePL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=LrGeAgent)


class LrLePLNetwork(BarabasiAlbert, LocalReputation, LocalEvolution, Network):
    """Scale-free network generated using a power law distribution with local reputation and local evolution."""

    name = "LrLePL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=LrLeAgent)


class GrLePLNetwork(BarabasiAlbert, GlobalReputation, LocalEvolution, Network):
    """Scale-free network generated using a power law distribution with global reputation and local reputation."""

    name = "GrLePL"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=GrLeAgent)


#####################################
## WATTS STROGATZ SMALL WORLD NETWORK
#####################################

class GrGeWSSWNetwork(WattsStrogatz, GlobalReputation, GlobalEvolution, Network):
    """Watts-Strogatz Small World model with Global Reputation and Global Evolution."""

    name = "GrGeWSSW"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=GrGeAgent)


class LrGeWSSWNetwork(WattsStrogatz, LocalReputation, GlobalEvolution, Network):
    """Watts-Strogatz Small World model with Local Reputation and Global Evolution."""

    name = "LrGeWSSW"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=LrGeAgent)


class LrLeWSSWNetwork(WattsStrogatz, LocalReputation, LocalEvolution, Network):
    """Watts-Strogatz Small World model with Local Reputation and Local Evolution."""

    name = "LrLeWSSW"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=LrLeAgent)


class GrLeWSSWNetwork(WattsStrogatz, GlobalReputation, LocalEvolution, Network):
    """Watts-Strogatz Small World model with Global Reputation and Local Evolution."""

    name = "GrLeWSSW"

    def __init__(self, _config=None):
        super().__init__(_config)
        self._generate(agentType=GrLeAgent)
