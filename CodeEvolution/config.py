from collections import namedtuple

import numpy as np

from .socialdilemna import PrisonersDilemma

Dilemma = namedtuple("Dilemma", ["type", "benefit", "cost"])
# State = namedtuple('State', ['mainID', 'proportion', 'mutantID'])
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
    """Configuration file describing a single parametrization of a simulation """

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
        degree: int = None,  # TODO: Change all the structure specific parameters into dictionary args
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
