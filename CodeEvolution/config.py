from CodeEvolution.socialdilemna import PrisonersDilemma

from collections import namedtuple
import numpy as np
import pickle

Dilemma = namedtuple('Dilemma', ['type', 'benefit', 'cost'])
State = namedtuple('State', ['mainID', 'proportion', 'mutantID'])
Population = namedtuple('Population', ['ID', 'proportion'])


class Config:
    """Configuration file describing a single parametrization of a simulation """

    def __init__(self,
                 initialState: State = State(mainID=0, proportion=0.9, mutantID=8),
                 size: int = 500,
                 densities: float = 1,
                 socialDilemma: Dilemma = Dilemma(type='PD', benefit=2, cost=1),
                 omegas: float = 0.99,
                 maxPeriods: int = 2000,
                 updateProbability: float = 0.1,
                 delta: float = 0.5,
                 mutationProbability: float = 0.1,
                 sparseDensity: bool = False,
                 degree: int = None,
                 attachment: int = None,
                 smallWorld: tuple = None) -> None:

        self.size = size
        self.population = Population(ID=initialState.mainID, proportion=initialState.proportion)
        self.mutant = Population(ID=initialState.mutantID, proportion=round(1 - initialState.proportion, 4))
        self.socialNormID = initialState.mainID  # Use the same social norm ID as the main strategy
        self.socialDilemma = PrisonersDilemma(socialDilemma.benefit, socialDilemma.cost)
        self.omega = omegas
        self.maxPeriods = maxPeriods
        self.updateProbability = updateProbability
        self.delta = delta
        self.mutationProbability = mutationProbability
        if sparseDensity:
            self.density = 2 * np.log(size) / size
        else:
            self.density = densities
        self.degree = degree
        self.attachment = attachment
        self.smallWorld = smallWorld

        if self.population.proportion + self.mutant.proportion != 1:
            total = self.population.proportion + self.mutant.proportion
            raise Exception(f"Population proportions sum to {total}, must sum to 1.")

    def __str__(self):
        s = ""
        for thing in self.__dict__.items():
            s += str(thing) + "\n"
        return s

    def __repr__(self):
        return str(self.__dict__)


if __name__ == "__main__":

    C = Config(initialState=State(mainID=7, proportion=1, mutantID=9))
    print(C)

# TODO: Add specific config files with parameters for all the extra structures! So extract the size, degree, density,
#  gamma, etc! or maybe just named tuples?
#