import logging

from .agent import Agent, GrGeAgent, LrGeAgent, GrLeAgent, LrLeAgent
from .evolution import GlobalEvolution, LocalEvolution
from .network import Network
from .reputation import GlobalReputation, LocalReputation
from .structures import ErdosRenyi, RandomRegularLattice, BarabasiAlbert, WattsStrogatz


#############################
## Model Constructor
#############################


class ceModel:
    mMap = {
        "structure": {
            "erdos renyi": ErdosRenyi,
            "reg lattice": RandomRegularLattice,
            "power law": BarabasiAlbert,
            "small world": WattsStrogatz,
        },
        "reputation": {
            "global": GlobalReputation,
            "local": LocalReputation,
        },
        "evolution": {
            "global": GlobalEvolution,
            "local": LocalEvolution,
        },
    }

    @staticmethod
    def build(config):
        structure = ceModel.mMap["structure"][config.structure]
        reputation = ceModel.mMap["reputation"][config.reputation]
        evolution = ceModel.mMap["evolution"][config.evolution]

        logging.info(
            f"Beginning Model Creation -> "
            f"Network({structure.__name__}, "
            f"{reputation.__name__}, "
            f"{evolution.__name__})"
        )

        class ConcreteAgent(evolution, Agent):
            def __init__(self, _id, _strategy):
                super().__init__(_id, _strategy)

        class ConcreteModel(structure, reputation, evolution, Network):
            def __init__(self, _config):
                logging.info("Concrete Model Created")
                super().__init__(_config)

        Model = ConcreteModel(config)
        Model._generate(ConcreteAgent)
        return Model


#############################
## Erdos Renyi Random Network
#############################


class GrGeERNetwork(ErdosRenyi, GlobalReputation, GlobalEvolution, Network):
    """Erdos Renyi Network with Global Reputation and Global Evolution"""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        config = _config
        if config.density != 1:
            logging.warning(
                f"Changing GrGeER Network density from {round(config.density, 3)} to 1"
            )
            config.density = 1  # Overwrite the density of any network run on GrGe to be fully connected
        if config.delta != 1:
            config.delta = 1
            logging.warning(
                "Delta (probability of successful reputation broadcast) is not 1, there will be errors!"
            )
        super().__init__(config)
        self._generate(agentType=GrGeAgent)


class LrGeERNetwork(ErdosRenyi, LocalReputation, GlobalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Global Evolution (LrGe)"""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=LrGeAgent)


class LrLeERNetwork(ErdosRenyi, LocalReputation, LocalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Local Evolution (LrLe)"""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=LrLeAgent)


class GrLeERNetwork(ErdosRenyi, GlobalReputation, LocalEvolution, Network):
    """Erdos Renyi Network with Local Reputation and Global Evolution (GrLe)"""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=GrLeAgent)


#############################
## D REGULAR LATTICE
#############################


class GrGeRRLNetwork(RandomRegularLattice, GlobalReputation, GlobalEvolution, Network):
    """Random d-regular lattice with global reputation and global evolution on a d-regular random lattice."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=GrGeAgent)


class LrGeRRLNetwork(RandomRegularLattice, LocalReputation, GlobalEvolution, Network):
    """Random d-regular lattice with Local Reputation and Global Evolution on a d-regular random lattice."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=LrGeAgent)


class LrLeRRLNetwork(RandomRegularLattice, LocalReputation, LocalEvolution, Network):
    """Random d-regular lattice with Local Reputation and Local Evolution on a d-regular random lattice."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=LrLeAgent)


class GrLeRRLNetwork(RandomRegularLattice, GlobalReputation, LocalEvolution, Network):
    """Random d-regular lattice with Global Reputation and Local Evolution on a d-regular random lattice."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=GrLeAgent)


#############################
## POWER LAW NETWORK
#############################


class GrGePLNetwork(BarabasiAlbert, GlobalReputation, GlobalEvolution, Network):
    """Scale-free network generated using a power law distribution with global reputation and global evolution."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=GrGeAgent)


class LrGePLNetwork(BarabasiAlbert, LocalReputation, GlobalEvolution, Network):
    """Scale-free network generated using a power law distribution with local reputation and global evolution."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=LrGeAgent)


class LrLePLNetwork(BarabasiAlbert, LocalReputation, LocalEvolution, Network):
    """Scale-free network generated using a power law distribution with local reputation and local evolution."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=LrLeAgent)


class GrLePLNetwork(BarabasiAlbert, GlobalReputation, LocalEvolution, Network):
    """Scale-free network generated using a power law distribution with global reputation and local reputation."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=GrLeAgent)


#####################################
## WATTS STROGATZ SMALL WORLD NETWORK
#####################################


class GrGeWSSWNetwork(WattsStrogatz, GlobalReputation, GlobalEvolution, Network):
    """Watts-Strogatz Small World model with Global Reputation and Global Evolution."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=GrGeAgent)


class LrGeWSSWNetwork(WattsStrogatz, LocalReputation, GlobalEvolution, Network):
    """Watts-Strogatz Small World model with Local Reputation and Global Evolution."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=LrGeAgent)


class LrLeWSSWNetwork(WattsStrogatz, LocalReputation, LocalEvolution, Network):
    """Watts-Strogatz Small World model with Local Reputation and Local Evolution."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=LrLeAgent)


class GrLeWSSWNetwork(WattsStrogatz, GlobalReputation, LocalEvolution, Network):
    """Watts-Strogatz Small World model with Global Reputation and Local Evolution."""

    def __init__(self, _config=None):
        logging.warning(
            f"Statically defined class {self.__class__.__name__} is deprecated. Use ceModel instead. "
        )
        super().__init__(_config)
        self._generate(agentType=GrLeAgent)
