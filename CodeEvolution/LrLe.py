import random

from CodeEvolution.network import Network
from CodeEvolution.configbuilder import ConfigBuilder
from CodeEvolution.agent import Agent
from CodeEvolution.results import Results
from CodeEvolution.socialnorm import SocialNorm
from CodeEvolution.socialdilemna import SocialDilemna, PrisonersDilemna
from CodeEvolution.strategy import Strategy

class LrLe_Network(Network):
	"""Network with Local Reputation and Local Evolution (LrLe)"""
	
	def __init__(self, _config):
		super().__init__(_config)
		self.createNetwork(agentType=None)
		self.evolutionaryUpdateSpeed = 0.5
			
	def evolutionaryUpdate(self):
		#TODO: COMPLETE
		for agent in self.agentList:
			agent.updateStrategy(self.config['updateProbability'], copyTheBest=True)
			
	def updateReputation(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
		"""Given the agents, their reputations, and their moves, update their personal reputations (the reputation they use for themselves for all of their interactions)."""

		agent1PersonalReputation = self.socialNorm.assignReputation(agent1.currentReputation, agent2Reputation, agent1Move)
		agent2PersonalReputation = self.socialNorm.assignReputation(agent2.currentReputation, agent1Reputation, agent2Move)

		agent1.updatePersonalReputation(agent1PersonalReputation)
		agent2.updatePersonalReputation(agent2PersonalReputation)

	def getOpponentsReputation(self, agent1, agent2):
		"""Local reputation - Calculate the reputation of your opponent given the last interaction of the opponent with a randomly chosen neighbour. Only when two agents are interacting are their H-Score is calculated through the social norm, each agent could be imbued with their own H-score attribute but don't think its necessary -> might be if it takes too long to calculate each time. If any agent's previous interaction with their randomly chosen neighbour doesn't exist, then randomly choose a reputation."""

		# Choose neighbour of each agent (except the opponent of that agent)
		agent2Neighbour = random.choice(agent2.neighbours)
		agent1Neighbour = random.choice(agent1.neighbours)
		while agent2Neighbour == agent1:
			agent2Neighbour = random.choice(agent2.neighbours)
		while agent1Neighbour == agent2:
			agent1Neighbour = random.choice(agent1.neighbours)

		# Get the agent's last interaction with their neighbour
		agent2ThirdPartyInteraction = agent2.history[agent2Neighbour]
		agent1ThirdPartyInteraction = agent1.history[agent1Neighbour]

		# Calculate agents' reputations using social norm, if no history, assign random reputation
		try:
			agent2PastReputation = agent2ThirdPartyInteraction['Focal Reputation']
			agent2NeighbourPastReputation = agent2ThirdPartyInteraction['Opponent Reputation']
			agent2PastMove = agent2ThirdPartyInteraction['Focal Move']
		except:
			# No history so randomly assign a reputation
			agent2Reputation = random.randint(0,1)
		else:
			agent2Reputation = self.socialNorm.assignReputation(agent2PastReputation, agent2NeighbourPastReputation, agent2PastMove)

		try:
			agent1PastReputation = agent1ThirdPartyInteraction['Focal Reputation']
			agent1NeighbourPastReputation = agent1ThirdPartyInteraction['Opponent Reputation']
			agent1PastMove = agent1ThirdPartyInteraction['Focal Move']
		except:
			agent1Reputation = random.randint(0,1)
		else:
			agent1Reputation = self.socialNorm.assignReputation(agent1PastReputation, agent1NeighbourPastReputation, agent1PastMove)

		return (agent1Reputation, agent2Reputation)

	def updateInteractions(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
		"""Following a game of a social dilemna between two agents, update the agents' reputations, utilities and record their interaction in their personal history log."""

		agent1Interaction = {
			'Opponent': agent2,
			'Focal Reputation': agent1.currentReputation,
			'Opponent Reputation': agent2Reputation,
			'Focal Move': agent1Move, 
			'Opponent Move': agent2Move
		}
		agent1.recordInteraction(agent1Interaction)		
		
		agent2Interaction = {
			'Opponent': agent1,
			'Focal Reputation': agent2.currentReputation,
			'Opponent Reputation': agent1Reputation,
			'Focal Move': agent2Move, 
			'Opponent Move': agent1Move
		}
		agent2.recordInteraction(agent2Interaction)	

if __name__=="__main__":
	
	# Social PrisonersDilemna
	pdBenefit = 2
	pdCost = 1

	# Network
	size = [50]
	density = [0.1] 
	distribution = [0.9, 0, 0, 0, 0, 0, 0, 0, 0.1, 0]
	socialNorm = 0
	omega = [0.99]

	# Model
	maxperiods = 10
	socialDilemna = PrisonersDilemna(pdBenefit, pdCost)
	updateProbability = [0.99]
	mutantID = 8
	probabilityOfMutants = [0.1]

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

	N = LrLe_Network(config)
	N.runSimulation()
	print(N)