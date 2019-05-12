import json
import datetime

class ConfigBuilder():
	
	def __init__(self, _sizes, _densities, _omegas, _singleSimulation=False, _saveToDisk=False):
		self.configuration = None

		isValid = self.__containsValidParameters(_sizes, _densities, _omegas)
		if not isValid:
			raise Exception("Parameters are invalid!")
		else:
			self.configuration = self.__generate(_sizes, _densities, _omegas)
			if _singleSimulation:
				self.configuration = self.configuration[0]

			if _saveToDisk:
				self.__getJsonConfigFile()

	def __generate(self, _sizes, _densities, _omegas):
		config = {}
		testCounter = 0
		for size in _sizes:
			for density in _densities:
				for omega in _omegas:
					config[testCounter] = {
						'size' : size,
						'density' : density,
						'omega' : omega
					}
					testCounter += 1
		return config

	def __getJsonConfigFile(self):
		timestamp = datetime.datetime.now()
		timestamp = timestamp.strftime("%d-%b-%Y (%H:%M:%S.%f)")
		with open('configurations/jsonConfig@{}.json'.format(timestamp), 'w') as jsonConfig:
			json.dump(self.config, jsonConfig, indent=4)

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

"""
TODO:

1. Redo the checking for single input or list of inputs
2. Redo the checking to raise exceptions and not to try to sanitise the input

"""

