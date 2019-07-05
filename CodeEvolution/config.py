
from CodeEvolution.socialdilemna import PrisonersDilemna

from collections import namedtuple

Dilemma = namedtuple('Dilemma', ['type', 'benefit', 'cost'])
Population = namedtuple('Population', ['mainID', 'mainProportion', 'mutantID', 'mutantProportion'])


class Config:

    def __init__(self,
                 size=500,
                 densities=1,
                 population=Population(mainID=0, mainProportion=0.9, mutantID=8, mutantProportion=0.1),
                 socialDilemma=Dilemma(type='PD', benefit=2, cost=1),
                 omegas=0.99,
                 maxPeriods=2000,
                 updateProbability=0.1,
                 probabilityOfMutants=1):

        if population.mainProportion + population.mutantProportion != 1:
            raise Exception("Population proportions do not sum to 1.")

        # TODO Validation checks (check validator class, should be able to just copy over)

        self.size = size
        self.density = densities
        self.population = population
        self.socialNormID = population.mainID  # Use the same social norm ID as the main strategy
        self.socialDilemma = PrisonersDilemna(socialDilemma.benefit, socialDilemma.cost)
        self.omega = omegas
        self.maxPeriods = maxPeriods
        self.updateProbability = updateProbability
        self.mutationProbability = probabilityOfMutants

    def __str__(self):
        return str(self.__dict__)


if __name__ == "__main__":

    C = Config()
    print(C)
