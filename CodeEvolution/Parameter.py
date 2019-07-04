from collections import namedtuple

populationDistribution = namedtuple('populationDistribution', ['mainID', 'mainProportion', 'mutantID',
                                                               'mutantProportion'])
socialDilemna = namedtuple('socialDilemna', ['type', 'benefit', 'cost'])


class Parameter:
    """Contains all the parameters for a single parameterised setup of the network simulation."""

    def __init__(self,
                 size=500,
                 density=0.1,
                 strategyDistribution=populationDistribution(mainID=0, mainProportion=0.9, mutantID=9,
                                                             mutantProportion=0.1),
                 socialDilemma=socialDilemna(type='prisonersDilemma', benefit=2, cost=1),
                 interactionProbability=0.99,
                 maxNoOfPeriods=2000,
                 updateProbability=0.1):

        self.size = size
        self.density = density
        self.strategyDistribution = strategyDistribution
        self.socialDilemma = socialDilemma
        self.interactionProbability = interactionProbability
        self.maxNoOfPeriods = maxNoOfPeriods
        self.updateProbability = updateProbability

    def __str__(self):
        s = str()
        s += str(self.size) + "\n"
        s += str(self.density) + "\n"
        s += str(self.strategyDistribution) + "\n"
        s += str(self.socialDilemma) + "\n"
        s += str(self.interactionProbability) + "\n"
        s += str(self.maxNoOfPeriods) + "\n"
        s += str(self.updateProbability) + "\n"
        return s


if __name__ == "__main__":

    p = Parameter()
    print(p)
