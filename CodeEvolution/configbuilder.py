import json

class ConfigBuilder():
	
	def __init__(self, _sizes, _densities, _omegas):
		self.isValid = self.containsValidParameters(_sizes, _densities, _omegas)
		if not self.isValid:
			raise Exception("Parameters are invalid!")
		else:
			self.config = self.generate(_sizes, _densities, _omegas)
			self.getJsonConfigFile()
			print("Success!")

	def generate(self, _sizes, _densities, _omegas):
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

	def getJsonConfigFile(self):
		with open('jsonConfig.json', 'w') as jsonConfig:
			json.dump(self.config, jsonConfig, indent=4)

	def containsValidParameters(self, _sizes, _densities, _omegas):
		ValidSizes = self.checkValidSizes(_sizes)
		ValidDensities = self.checkValidDensities(_densities)
		ValidOmegas = self.checkValidOmegas(_omegas)
		return True if ValidSizes and ValidDensities and ValidOmegas else False

	def checkValidSizes(self, _sizes):
		isPositive = all(i >= 3 for i in _sizes)
		isInt = all(type(i) == int for i in _sizes)
		return True if isPositive and isInt else False

	def checkValidDensities(self, _densities):
		inRange = all(i > 0 and i <= 1 for i in _densities)
		return True if inRange else False

	def checkValidOmegas(self, _omegas):
		inRange = all(i > 0 and i < 1 for i in _omegas)
		return True if inRange else False


sizes = [3, 4, 10000]
densities = [0.5]
omegas = [0.5]

obj = ConfigBuilder(sizes, densities, omegas)









