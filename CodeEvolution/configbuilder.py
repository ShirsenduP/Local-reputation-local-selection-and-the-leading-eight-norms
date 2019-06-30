import json
import datetime
from CodeEvolution.socialdilemna import PrisonersDilemna
from CodeEvolution.validator import Validator

class ConfigBuilder():
    
    def __init__(self,
        _sizes=[500],
        _densities=[0.2],
        _distributions=[[0.9, 0, 0, 0, 0, 0, 0, 0, 0.1, 0]],
        _socialNorm=0,
        _socialDilemna=('PD', 2, 1), 
        _omegas=[0.99], 
        _maxperiods=2000, 
        _updateProbability=[0.1],
        _mutantID=8,
        _probabilityOfMutants=[1]):
        
        self.configuration = self.__generate(_sizes, 
            _densities,
            _distributions, 
            _socialNorm,
            _omegas, 
            _maxperiods, 
            _socialDilemna,
            _updateProbability,
            _mutantID,
            _probabilityOfMutants)

    def __generate(self, _sizes, _densities, _distributions, _socialNorm, _omegas, _maxperiod, _socialDilemna, _updateProbability, _mutantID, _probabilityOfMutants):
        config = {}
        testCounter = 0
        for size in _sizes:
            for density in _densities:
                for omega in _omegas:
                    for updateProbability in _updateProbability:
                        for probabilityOfMutants in _probabilityOfMutants:
                            for _distribution in _distributions:
                                config[testCounter] = {
                                    'size' : size,
                                    'density' : density,
                                    'distribution' : _distribution,
                                    'socialNorm' : _socialNorm,
                                    'socialDilemna' : _socialDilemna,
                                    'omega' : omega,
                                    'maxperiods' : _maxperiod,
                                    'dilemna' : _socialDilemna,
                                    'updateProbability' : updateProbability,
                                    'mutantID' : _mutantID,
                                    'probabilityOfMutants' : probabilityOfMutants
                                }
                                testCounter += 1

        if testCounter == 1:
            return config[0]
        else:        
            return config


if __name__ == "__main__":

    def distributionExperimentConfig(self, mutantWeight=0.1):
        tests = [[1-mutantWeight,0,0,0,0,0,0,0,mutantWeight,0],
                [0,1-mutantWeight,0,0,0,0,0,0,mutantWeight,0],
                [0,0,1-mutantWeight,0,0,0,0,0,mutantWeight,0],
                [0,0,0,1-mutantWeight,0,0,0,0,mutantWeight,0],
                [0,0,0,0,1-mutantWeight,0,0,0,mutantWeight,0],
                [0,0,0,0,0,1-mutantWeight,0,0,mutantWeight,0],
                [0,0,0,0,0,0,1-mutantWeight,0,mutantWeight,0],
                [0,0,0,0,0,0,0,1-mutantWeight,mutantWeight,0]]
        return tests

    s = distributionExperimentConfig(0.3)
    print(s)