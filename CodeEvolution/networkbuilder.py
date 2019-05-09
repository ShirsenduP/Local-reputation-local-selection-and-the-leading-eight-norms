import yaml

class NetworkBuilder():

	def __init__(self, _configYAML):
		self.loadYAML(configYAML)
		self.size = None
		self.density
		self.omega
		self.currentTimeStep = 0

	def loadYAML(self, _configYAML):
		with open(_configYAML, 'r') as config:
			try:
				self.size = None
				self.density = None
				self.omega = None
			except yaml.YAMLError as exc:
				print(exc)
"""
TODO:

1. Need to rewrite this to use JSON, not yaml, what is the purpose of this class?
2. Plan

	Input:

		dictionary containing all parameters 
"""
