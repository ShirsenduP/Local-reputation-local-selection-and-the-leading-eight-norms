import json
import datetime

class ConfigBuilder():
	
	def __init__(self, 
		_sizes, 
		_densities, 
		_distribution,
		_socialNorm,
		_omegas, 
		_maxperiods, 
		_socialDilemna, 
		_updateProbability,
		_mutantID,
		_probabilityOfMutants,
		_saveToDisk=False):

		self.configuration = self.__generate(_sizes, 
			_densities,
			_distribution, 
			_socialNorm,
			_omegas, 
			_maxperiods, 
			_socialDilemna,
			_updateProbability,
			_mutantID,
			_probabilityOfMutants)



	def __generate(self, _sizes, _densities, _distribution, _socialNorm, _omegas, _maxperiod, _socialDilemna, _updateProbability, _mutantID, _probabilityOfMutants):
		config = {}
		testCounter = 0
		for size in _sizes:
			for density in _densities:
				for omega in _omegas:
					for updateProbability in _updateProbability:
						for probabilityOfMutants in _probabilityOfMutants:
							# print(testCounter)
							config[testCounter] = {
								'size' : size,
								'density' : density,
								'distribution' : _distribution,
								'socialNorm' : _socialNorm,
								'omega' : omega,
								'maxperiods' : _maxperiod,
								'dilemna' : _socialDilemna,
								'updateProbability' : updateProbability,
								'mutantID' : _mutantID,
								'probabilityOfMutants' : probabilityOfMutants
							}
							testCounter += 1
							
		return config


def main():
	pass

if __name__ == "__main__":
	main()

