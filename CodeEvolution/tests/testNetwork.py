from CodeEvolution.agent import Agent
from CodeEvolution.network import Network
from CodeEvolution.socialdilemna import PrisonersDilemna
from CodeEvolution.configbuilder import ConfigBuilder

from unittest import TestCase
import random
import numpy as np


# Random Number Generation (seed must be 1 for testing)
seed = 1
random.seed(seed)
np.random.seed(seed)

# Social PrisonersDilemna
pdBenefit = 2
pdCost = 1

# Network
size = [5]
density = [1] 
distribution = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
socialNorm = 0

# Model
omega = [0.5]
maxperiods = 1
socialDilemna = PrisonersDilemna(pdBenefit, pdCost)
updateProbability = [0.1]
mutantID = 8
probabilityOfMutants = [0.1]

def DefaultTestNetwork(size=size, 
	density=density,
	distribution=distribution,
	socialNorm=socialNorm,
	omega=omega, 
	maxperiod=maxperiods,
	socialDilemna=socialDilemna,
	updateProbability=updateProbability,
	mutantID=mutantID,
	probabilityOfMutants=probabilityOfMutants):
	"""This function creates a default network with the parameters defined above. For one-off test cases with different parameterisations, pass in the new value for any of the parameters to create a custom network. Otherwise, call with no arguments to create a default network setup."""
	
	if seed != 1:
		raise ValueError("Seed not initialised to correct default value (1)!")

	config = ConfigBuilder(
		_sizes=size,
		_densities=density,
		_distribution=distribution,
		_socialNorm=socialNorm,
		_omegas=omega,
		_maxperiods=maxperiod,
		_socialDilemna=socialDilemna,
		_updateProbability=updateProbability,
		_mutantID=mutantID,
		_probabilityOfMutants=probabilityOfMutants)

	config = config.configuration[0]
	N = Network(config)
	return N


class NetworkTest(TestCase):

	def testNetworkInitialisation(self):
		N = DefaultTestNetwork()
		self.assertEqual(len(N.agentList), size[0])
		self.assertEqual(N.socialNorm.stateID, socialNorm)
		self.assertEqual(N.currentPeriod, 0)

		# for agent in N.agentList:
		# 	self.assertEqual(agent.currentStrategy.currentStrategyID, 0)
		
		customSize = [50]
		customDistribution = [0.2, 0.2, 0.0, 0.0, 0.2, 0.1, 0.1, 0.1, 0.1, 0.0]
		N = DefaultTestNetwork(size=customSize, distribution=customDistribution)
		strategies = [agent.currentStrategy.currentStrategyID for agent in N.agentList]
		strategyCounts = [strategies.count(val) for val in range(len(customDistribution))]

		actualCounts = [val*customSize[0] for val in customDistribution]
		self.assertEqual(strategyCounts, actualCounts)

	def testCheckMinTwoNeighbours(self):
		with self.assertRaises(Exception) as err:
			DefaultTestNetwork(size=[0])
			DefaultTestNetwork(size=[1])
			DefaultTestNetwork(size=[2])
			DefaultTestNetwork(size=[10], density=[0.1])
			DefaultTestNetwork(size=[10], density=[0.5])
			DefaultTestNetwork(size=[1000], density=[0])


	def testResetTempActions(self):
		"""In this test, with seed=1, agents 3 and 4 interact first and they both cooperate"""
		N = DefaultTestNetwork()

		self.assertEqual(N.tempActions['C'], 0)
		self.assertEqual(N.tempActions['D'], 0)
		N.runSingleTimestep()
		self.assertEqual(N.tempActions['C'], 2)
		self.assertEqual(N.tempActions['D'], 0)
		N.resetTempActions()
		self.assertEqual(N.tempActions['C'], 0)
		self.assertEqual(N.tempActions['D'], 0)
		N.resetTempActions()
		self.assertEqual(N.tempActions['C'], 0)
		self.assertEqual(N.tempActions['D'], 0)

		for interaction in range(random.randint(1,100)):
			N.runSingleTimestep()
		
		self.assertNotEqual(N.tempActions['C'], 0)
		self.assertNotEqual(N.tempActions['D'], 0)
		N.resetTempActions()
		self.assertEqual(N.tempActions['C'], 0)
		self.assertEqual(N.tempActions['D'], 0)

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