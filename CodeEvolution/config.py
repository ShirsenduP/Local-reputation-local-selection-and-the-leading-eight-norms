from CodeEvolution.socialdilemna import PrisonersDilemma

from collections import namedtuple

Dilemma = namedtuple('Dilemma', ['type', 'benefit', 'cost'])
State = namedtuple('InitialState', ['mainID', 'proportion', 'mutantID'])
Population = namedtuple('Population', ['ID', 'proportion'])


class Config:

    def __init__(self,
                 initialState=State(mainID=0, proportion=0.9, mutantID=8),
                 size=500,
                 densities=1,
                 socialDilemma=Dilemma(type='PD', benefit=2, cost=1),
                 omegas=0.99,
                 maxPeriods=2000,
                 updateProbability=0.1,
                 probabilityOfMutants=1):

        # TODO Validation checks (check validator class, should be able to just copy over)
        self.size = size
        self.density = densities
        self.population = Population(ID=initialState.mainID, proportion=initialState.proportion)
        self.mutant = Population(ID=initialState.mutantID, proportion=round(1-initialState.proportion, 4))
        self.socialNormID = initialState.mainID  # Use the same social norm ID as the main strategy
        self.socialDilemma = PrisonersDilemma(socialDilemma.benefit, socialDilemma.cost)
        self.omega = omegas
        self.maxPeriods = maxPeriods
        self.updateProbability = updateProbability
        self.mutationProbability = probabilityOfMutants

        if self.population.proportion + self.mutant.proportion != 1:
            raise Exception(f"Population proportions are {self.population.proportion} + {self.mutant.proportion} != 1")

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


if __name__ == "__main__":

    C = Config(initialState=State(mainID=7, proportion=1, mutantID=9))
    print(C)
