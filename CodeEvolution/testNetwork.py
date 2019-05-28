from agent import Agent
from network import Network
from socialdilemna import PrisonersDilemna
from configbuilder import ConfigBuilder

from unittest import TestCase
import random
import numpy as np

class NetworkTest(TestCase):
	def setUp(self):
		print("setup")
		self.seed = 1
		random.seed(self.seed)
		np.random.seed(self.seed)

		# Social PrisonersDilemna
		self.pdBenefit = 1
		self.pdCost = 0.5

		# Network
		self.size = [5]
		self.density = [0.8] 
		self.distribution = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.socialNorm = 0

		# Model
		self.omega = [0.5]
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

	def testNetworkInitialisation(self):

		self.assertEqual(self.seed, 1)
		self.assertEqual(len(self.N.agentList), self.size[0])
		self.assertEqual(self.N.socialNorm.stateID, self.socialNorm)
		self.assertEqual(self.N.currentPeriod, 0)

		for agent in self.N.agentList:
			self.assertEqual(agent.currentStrategy.currentStrategyID, 0)
		
	
	def testCheckMinTwoNeighbours(self):
		pass

	def testResetTempActions(self):
		pass

	def testInitstrategies(self):
		pass

	def testScanStrategies(self):
		pass

	def testCompareNetworkStats(self):
		pass

	def testRunSimulation(self):
		pass
	
	def testErdosRenyiGenerator(self):
		pass

	def testGetOpponentsReputation(self):
		pass

	def testPlaySocialDilemna(self):
		pass

	def testShowHistory(self):
		pass

	def testCheckConvergence(self):
		pass

	def testChooseTwoAgents(self):
		pass

	def testAddMutants(self):
		pass

	def testRunSingleTimestep(self):
		pass

	def testResetUtility(self):
		pass

	def testGrabSnapshot(self):
		pass

	def testInitialiseAgentHistories(self):
		pass