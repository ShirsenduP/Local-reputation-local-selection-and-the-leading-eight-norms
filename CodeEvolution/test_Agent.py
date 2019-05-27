from agent import Agent
from network import Network
from socialdilemna import PrisonersDilemna
from configbuilder import ConfigBuilder

from unittest import TestCase
import random
import numpy as np

class agentTest(TestCase):
	def setUp(self):

		seed = 1
		random.seed(seed)
		np.random.seed(seed)

		# Social PrisonersDilemna
		self.pdBenefit = 1
		self.pdCost = 0.5

		# Network
		self.size = [5]
		self.density = [0.8] 
		self.distribution = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.socialNorm = 0
		self.omega = [0.5]

		# Model
		self.maxperiods = 1
		self.socialDilemna = PrisonersDilemna(self.pdBenefit, self.pdCost)
		self.updateProbability = [0.1]
		self.mutantID = 8
		self.probabilityOfMutants = [0.1]
		self.singleSimulation = True

		config = ConfigBuilder(
			_sizes=self.size,
			_densities=self.density,
			_distribution=self.distribution,
			_socialNorm=self.socialNorm,
			_omegas=self.omega,
			_maxperiods=self.maxperiods,
			_socialDilemna=self.socialDilemna,
			_updateProbability=self.updateProbability,
			_mutantID=self.mutantID,
			_probabilityOfMutants=self.probabilityOfMutants)

		config = config.configuration[0]
		self.N = Network(_config=config)

	def testAgentInitialisation(self):
		self.assertEqual(len(self.N.agentList), self.size[0])
		self.assertEqual(self.N.socialNorm.stateID, self.socialNorm)
		self.assertEqual(self.N.currentPeriod, 0)
		