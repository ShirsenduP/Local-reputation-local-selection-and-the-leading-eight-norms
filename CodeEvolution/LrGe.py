import random

from CodeEvolution.network import Network
from CodeEvolution.configbuilder import ConfigBuilder
from CodeEvolution.agent import Agent
from CodeEvolution.results import Results
from CodeEvolution.socialnorm import SocialNorm
from CodeEvolution.socialdilemna import SocialDilemna, PrisonersDilemna
from CodeEvolution.strategy import Strategy

class LrGe_Network(Network):
	"""Network with Local Reputation and Global Evolution (LrGe)"""
	
	def __init__(self, config):
		raise NotImplementedError

	def getOpponentsReputation(self):
		raise NotImplementedError

	def updateInteractions(self):
		raise NotImplementedError
	
	def updateReputation(self):
		raise NotImplementedError

	def evolutionaryUpdate(self):
		raise NotImplementedError

if __name__=="__main__":
	pass