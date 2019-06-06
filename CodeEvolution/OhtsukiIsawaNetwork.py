import random

from CodeEvolution.network import Network
from CodeEvolution.configbuilder import ConfigBuilder
from CodeEvolution.agent import Agent
from CodeEvolution.results import Results
from CodeEvolution.socialnorm import SocialNorm
from CodeEvolution.socialdilemna import SocialDilemna, PrisonersDilemna
from CodeEvolution.strategy import Strategy

class OhtsukiIsawaNetwork(Network):
	
	def __init__(self, _config):
		super().__init__(_config)
		if _config['density'] != 1:
			_config['density'] = 1
		self.createNetwork()
		self.evolutionaryUpdateSpeed = 0.5
	
	def createNetwork(self):
		"""Generate a fully connected graph (density = 1)"""
		strategyDistribution = self.getStrategyCounts()
		for agentID in range(self.config['size']):
			randomStrategyIndex = random.randint(0, len(strategyDistribution)-1)
			self.agentList.append(OhtsukiIsawaAgent(_id=agentID, _strategy=strategyDistribution[randomStrategyIndex]))
			strategyDistribution.pop(randomStrategyIndex)
			self.population.add_node(self.agentList[agentID])

		for agentID1 in range(len(self.population)):
			for agentID2 in range(len(self.population)):
				if agentID1 != agentID2:
					r = random.random()
					if r < self.config['density']:
						self.population.add_edge(self.agentList[agentID1], self.agentList[agentID2])
						if self.agentList[agentID2] not in self.agentList[agentID1].neighbours:
							self.agentList[agentID1].neighbours.append(self.agentList[agentID2])
						if self.agentList[agentID1] not in self.agentList[agentID2].neighbours:
							self.agentList[agentID2].neighbours.append(self.agentList[agentID1])

	def getOpponentsReputation(self, agent1, agent2):
		"""Return the reputations of the two randomly chosen agents."""
		return agent1.currentReputation, agent2.currentReputation

	def runSimulation(self):
		"""Run full simulation for upto total number of simulations defined in 'self.config['maxperiods']' or up until the system converges at preallocated randomly chosen convergence check intervals."""
		self.initStrategies()
		self.scanStrategies()
		mutantProbability = self.config['probabilityOfMutants']
		while self.currentPeriod < self.config['maxperiods'] and not self.hasConverged:
			self.resetUtility()
			self.resetTempActions()
			self.runSingleTimestep()
			self.scanStrategies()
			r = random.random()
			if r < mutantProbability:
				self.addMutants(self.config['mutantID'], mutantProbability)
			# self.results.updateActions(self.tempActions)
			self.evolutionaryUpdate(self.evolutionaryUpdateSpeed)

			if self.currentPeriod in self.convergenceCheckIntervals:
				self.grabSnapshot()
				self.checkConvergence()
			
			if self.hasConverged or self.currentPeriod==self.config['maxperiods']-1:
				self.results.convergedAt = self.currentPeriod
				return
			else: 
				self.currentPeriod += 1

	def playSocialDilemna(self):
		agent1, agent2 = self.chooseTwoAgents()
		agent1Reputation, agent2Reputation = self.getOpponentsReputation(agent1, agent2)
		agent1Move = agent1.currentStrategy.chooseAction(agent1Reputation, agent2Reputation)
		agent2Move = agent2.currentStrategy.chooseAction(agent2Reputation, agent1Reputation)
		self.tempActions[agent1Move] += 1
		self.tempActions[agent2Move] += 1

		payoff1, payoff2 = self.config['dilemna'].playGame(agent1Move, agent2Move)

		agent1.updateUtility(payoff1)
		agent2.updateUtility(payoff2)

		# print(f"Agent {agent1.id} has reputation {agent1.currentReputation}, made move {agent1Move} and got payoff {payoff1}")
		# print(f"Agent {agent2.id} has reputation {agent2.currentReputation}, made move {agent2Move} and got payoff {payoff2}")

		agent1NewReputation = self.socialNorm.assignReputation(agent1Reputation, agent2Reputation, agent1Move)
		agent2NewReputation = self.socialNorm.assignReputation(agent2Reputation, agent1Reputation, agent2Move)

		agent1.updateReputation(agent1NewReputation)
		agent2.updateReputation(agent2NewReputation)

class OhtsukiIsawaAgent(Agent):

	def __init__(self, _id, _strategy):
		super().__init__(_id, _strategy)
		self.history = None
		self.currentReputation = random.choice(self.reputation)

	def initialiseHistory(self):
		pass

	def updateReputation(self, newRep):
		self.currentReputation = newRep

	def updateStrategy(self, updateProbability):
		"""Overwrite the default update strategy method which implements local learning. Strategy updates occur in the network.evolutionaryUpdate method."""
		pass






if __name__ == "__main__":
	
	# Social PrisonersDilemna
	pdBenefit = 2
	pdCost = 1

	# Network
	size = [100]
	density = [1] 
	distribution = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	socialNorm = 0
	omega = [0.99]

	# Model
	maxperiods = 5
	socialDilemna = PrisonersDilemna(pdBenefit, pdCost)
	updateProbability = [0.1]
	mutantID = 8
	probabilityOfMutants = [0.2]

	#TODO TESTS
	"""	1. starting 50/50 mutants and some Strategy
		2. Initially a strategy and no mutants - at the end of each timestep, each agent has some 'probabilityOfMutants' of turning into a mutant (<< .1 )
		3. test the number of mutants needed to kill the system"""


	###
	### MODEL-GENERATED-PARAMETERS
	###

	config = ConfigBuilder(
		_sizes=size,
		_densities=density,
		_distribution=distribution,
		_socialNorm=socialNorm,
		_omegas=omega,
		_maxperiods=maxperiods,
		_socialDilemna=socialDilemna,
		_updateProbability=updateProbability,
		_mutantID=mutantID,
		_probabilityOfMutants=probabilityOfMutants)

	config = config.configuration[0]

	print("START OHTSUKI AND ISAWA MODEL")
	N = OhtsukiIsawaNetwork(config)
	print("Starting Strategy Distribution (T=0) - ", N.getCensus())
	N.runSimulation()
	print(f"Ending Strategy Distribution (T={N.results.convergedAt}) - ", N.getCensus())
	print("END")
