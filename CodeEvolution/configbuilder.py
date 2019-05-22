import json
import datetime

class ConfigBuilder():
	
	def __init__(self, 
		_sizes, 
		_densities, 
		_distribution,
		_omegas, 
		_maxperiods, 
		_socialDilemna, 
		_updateProbability,
		_mutantID,
		_probabilityOfMutants,
		_singleSimulation=False, 
		_saveToDisk=False):
		
		# TODO: raise exceptions for invalid parameters! 

		self.configuration = None

		isValid = self.__containsValidParameters(_sizes, _densities, _omegas)
		if not isValid:
			raise Exception("Parameters are invalid!")
		else:
			self.configuration = self.__generate(_sizes, 
				_densities,
				_distribution, 
				_omegas, 
				_maxperiods, 
				_socialDilemna,
				_updateProbability,
				_mutantID,
				_probabilityOfMutants)

			if _singleSimulation:
				self.configuration = self.configuration[0]


	def __generate(self, _sizes, _densities, _distribution, _omegas, _maxperiod, _socialDilemna, _updateProbability, _mutantID, _probabilityOfMutants):
		config = {}
		testCounter = 0
		for size in _sizes:
			for density in _densities:
				for omega in _omegas:
					for updateProbability in _updateProbability:
						for probabilityOfMutants in _probabilityOfMutants:
							print(testCounter)
							config[testCounter] = {
								'size' : size,
								'density' : density,
								'distribution' : _distribution,
								'omega' : omega,
								'maxperiods' : _maxperiod,
								'dilemna' : _socialDilemna,
								'updateProbability' : updateProbability,
								'mutantID' : _mutantID,
								'probabilityOfMutants' : probabilityOfMutants
							}
							testCounter += 1
							
		return config

	def __containsValidParameters(self, _sizes, _densities, _omegas):
		ValidSizes = self.__checkValidSizes(_sizes)
		ValidDensities = self.__checkValidDensities(_densities)
		ValidOmegas = self.__checkValidOmegas(_omegas)
		return True if ValidSizes and ValidDensities and ValidOmegas else False

	def __checkValidSizes(self, _sizes):
		isPositive = all(size >= 3 for size in _sizes)
		isInt = all(type(size) == int for size in _sizes)
		return True if isPositive and isInt else False

	def __checkValidDensities(self, _densities):
		inRange = all(density > 0 and density <= 1 for density in _densities)
		return True if inRange else False

	def __checkValidOmegas(self, _omegas):
		inRange = all(omega > 0 and omega < 1 for omega in _omegas)
		return True if inRange else False


def main():
	pass

if __name__ == "__main__":
	main()

