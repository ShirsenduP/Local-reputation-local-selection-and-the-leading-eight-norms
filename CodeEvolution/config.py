from collections import namedtuple

import numpy as np

from .socialdilemna import PrisonersDilemma

Dilemma = namedtuple("Dilemma", ["type", "benefit", "cost"])
Population = namedtuple("Population", ["ID", "proportion"])


class State:
    def __init__(self, mainID, proportion, mutantID):
        self.mainID = mainID
        self.proportion = proportion
        self.mutantID = mutantID

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"mainID={self.mainID}, "
            f"proportion={self.proportion}, "
            f"mutantID={self.mutantID})"
        )


class Config:
    """
    Configuration file describing a single parametrization of a simulation.

    Args:
        testcase (str):
            Shortcut for a quick configuration. Can be "minimal" or "grle"
        structure (str):
            Name of structure of network. If reputation and evolution are set to global, then this has no effect.
        reputation (str):
            Sets the reputation mechanism, can be either `global` or `local`.
        evolution (str):
            Sets the evolution mechanism, can be either `global` or `local`.
        size (int):
            Size of the population (size > 0).
        initialState (State):
            Initial state of the population.
        socialDilemma (Dilemma):
            Configuration of the social dilemma used. Only Prisoner's Dilemma is implemented currently.
        omegas (float):
            Probability of further interactions in the same time-step (0 <= omegas < 1).
        maxPeriods (int):
            Maximum number of time-steps to simulate assuming no early termination due to convergence (maxPeriods > 0).
        alpha (float):
            Speed of evolutionary update (0 <= alpha <= 1).
        delta (float):
            Probability of reputation broadcast (0 <= delta <= 1).
        mutationProbability (float):
            Probability of a random unconditional defector spawning in the population in a single
            timestep (0 <= mutationProbability <= 1).
        density (float):
            Density of the erdos renyi random graph (0 < density <= 1). If density is 1, then it is a fully
            connected graph.
        sparseDensity (bool):
            If True, then the density of the erdos renyi random graph is set to be 2*log(N)/N where N is the size of the
            population. This is shown to be the minimum density for the graph to be connected.
        degree (int):
            If structure is 'reg lattice', `degree` is the degree of the random regular lattice.
        attachment (int):
            Preferential attachment parameter in Barabasi Albert network. Nodes added by preferentially adding
            `attachment` edges to existing nodes with high degree.
        smallWorld (tuple[int, float]):
            Each node in the graph is connected to its `smallWorld[0]` neighbours in a ring topology. Their edges are
            then rewired randomly with probability `smallWorld[1]`.
    """

    yaml_tag = "!Config"

    def __init__(
        self,
        testcase: str = None,
        structure: str = None,
        reputation: str = None,
        evolution: str = None,
        size: int = 300,
        initialState: State = State(mainID=0, proportion=1, mutantID=8),
        socialDilemma: Dilemma = Dilemma(type="PD", benefit=2, cost=1),
        omegas: float = 0.99,
        maxPeriods: int = 2000,
        alpha: float = 0.1,
        delta: float = 1,
        mutationProbability: float = 0.1,
        density: float = None,
        sparseDensity: bool = True,
        degree: int = None,
        attachment: int = None,
        smallWorld: tuple = None,
    ) -> None:

        if testcase == "minimal":
            self.structure = "erdos renyi"
            self.reputation = "global"
            self.evolution = "global"
            self.size = 100
            self.population = Population(ID=0, proportion=1)
            self.mutant = Population(ID=8, proportion=0)
            self.socialNormID = initialState.mainID
            self.socialDilemma = PrisonersDilemma(2, 1)
            self.omega = 0.99
            self.maxPeriods = 100
            self.alpha = 0.1
            self.delta = 0.5
            self.mutationProbability = 0.1
            self.density = 1
            self.degree = None
            self.attachment = None
            self.smallWorld = None
            return
        elif testcase == "grle":
            self.structure = "erdos renyi"
            self.reputation = "global"
            self.evolution = "local"
            self.size = 100
            self.population = Population(ID=0, proportion=1)
            self.mutant = Population(ID=8, proportion=0)
            self.socialNormID = initialState.mainID
            self.socialDilemma = PrisonersDilemma(2, 1)
            self.omega = 0.99
            self.maxPeriods = 100
            self.alpha = 0.1
            self.delta = 0.5
            self.mutationProbability = 0.1
            self.density = 1
            self.degree = None
            self.attachment = None
            self.smallWorld = None
            return
        else:
            self.structure = structure
            self.reputation = reputation
            self.evolution = evolution
            self.size = size
            self.population = Population(
                ID=initialState.mainID, proportion=initialState.proportion
            )
            self.mutant = Population(
                ID=initialState.mutantID,
                proportion=round(1 - initialState.proportion, 4),
            )
            # Use the same social norm ID as the main strategy
            self.socialNormID = initialState.mainID
            self.socialDilemma = PrisonersDilemma(
                socialDilemma.benefit, socialDilemma.cost
            )
            self.omega = omegas
            self.maxPeriods = maxPeriods
            self.alpha = alpha
            self.delta = delta
            self.mutationProbability = mutationProbability
            self.sparseDensity = sparseDensity
            if sparseDensity:
                self.density = 2 * np.log(size) / size
            else:
                self.density = density
            self.degree = degree
            self.attachment = attachment
            self.smallWorld = smallWorld

            if self.population.proportion + self.mutant.proportion != 1:
                total = self.population.proportion + self.mutant.proportion
                raise Exception(
                    f"Population proportions sum to {total}, must sum to 1."
                )

    def __str__(self):
        s = ""
        for thing in self.__dict__.items():
            s += str(thing) + "\n"
        return s

    def __repr__(self):
        return str(self.__dict__)
