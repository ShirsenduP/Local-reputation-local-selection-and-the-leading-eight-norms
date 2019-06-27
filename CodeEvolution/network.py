import copy
import random
import logging
import numpy as np
import time 
from collections import deque, namedtuple

import matplotlib.pyplot as plt
import networkx as nx

from CodeEvolution.agent import Agent
from CodeEvolution.results import Results
from CodeEvolution.socialnorm import SocialNorm
from CodeEvolution.socialdilemna import SocialDilemna, PrisonersDilemna
from CodeEvolution.strategy import Strategy

class Network():

	def __init__(self, _config, agentType=Agent):
		self.config = _config.configuration
		self.mainStratIDs = self.strategiesInPopulation()
		self.agentList = []
		self.socialNorm = SocialNorm(self.mainStratIDs[0])
		self.population = nx.Graph()
		self.currentPeriod = 0	
		self.results = Results([self.mainStratIDs[0], self.mainStratIDs[1]])
		self.tempActions = {'C' : 0, 'D' : 0}
		self.hasConverged = False
		self.convergenceCheckIntervals = random.sample(range(int(self.config['maxperiods']/4),self.config['maxperiods']), int(self.config['maxperiods']/100))
		self.convergenceCheckIntervals.sort()
		self.convergenceHistory = deque(3*[None], 3)
		self.utilityMonitor = [{}.fromkeys(range(10), 0), {}.fromkeys(range(10), 0)] #index0 captures #OfInteractions of an agent with some strategy, index1 captures the total cumulative payoff of all agents running that strategy
		dilemnaParameters = self.config['socialDilemna']
		if dilemnaParameters[0] == 'PD':
			self.dilemna = PrisonersDilemna(dilemnaParameters[1], dilemnaParameters[2])
		else:
			raise Exception("Social dilemna invalid, must be 'PD' currently!")
		

	def strategiesInPopulation(self):
		"""Find the main strategy ID in the population"""
		dist = self.config['distribution'] #Only want to find non-mutant agents in the populatiob
		strategies = [dist.index(value) for value in dist if value != 0]
		if len(strategies) > 2:
			raise Exception("More than 1 non-mutant agent in the strategy")
		return strategies[0], strategies[1]



	def __del__(self):
		self.socialNorm = None
		self.currentPeriod = 0
		self.results = None
		self.resetTempActions()
		self.hasConverged = False 
		Strategy.reset()
		

	def resetTempActions(self):
		"""Reset the cooperation/defection counter to zero. To be used at the end of each timeperiod after actions have been recorded."""

		for action in self.tempActions:
			self.tempActions[action] = 0

	def scanStrategies(self):
		"""Update the results with the proportions of all strategies at any given time."""

		#update results with census		
		census = self.getCensusProportions()
		self.results.strategyProportions[self.currentPeriod] = census
		
		# #add up all the utilities over the strategies
		# censusCounts = self.getCensus()
		# averageUtilities = {}.fromkeys(censusCounts.keys(), 0)
		# for agent in self.agentList:
		# 	agentStratID = agent.currentStrategy.currentStrategyID
		# 	averageUtilities[agentStratID] += agent.currentUtility
			
		# #average the utilities
		# for ID, _ in averageUtilities.items():
		# 	if censusCounts[ID] > 0:
		# 		averageUtilities[ID] /= censusCounts[ID]

		# #update results with utilities
		# self.results.utilities[self.currentPeriod] = averageUtilities

		interactionsDict = self.utilityMonitor[0]
		payoffDict = self.utilityMonitor[1]
		averageUtilities = {}.fromkeys(range(10), 0)

		for key, _ in averageUtilities.items():
			if interactionsDict[key]:
				averageUtilities[key] = payoffDict[key]/interactionsDict[key]
		self.results.utilities[self.currentPeriod] = averageUtilities
		

	def runSimulation(self):
		"""Run full simulation for upto total number of simulations defined in 'self.config['maxperiods']' or up until the system converges at preallocated randomly chosen convergence check intervals."""
		self.scanStrategies()
		mutantProbability = self.config['probabilityOfMutants']
		while self.currentPeriod < self.config['maxperiods'] and not self.hasConverged:
			self.resetUtility()
			self.resetTempActions()
			self.runSingleTimestep()
			self.scanStrategies()
			self.mutation(self.config['mutantID']) 
			self.evolutionaryUpdate()
			if self.currentPeriod in self.convergenceCheckIntervals:
				self.grabSnapshot()
				self.checkConvergence()
			
			if self.hasConverged or self.currentPeriod==self.config['maxperiods']-1:
				self.results.convergedAt = self.currentPeriod
				break
			else: 
				self.currentPeriod += 1
		
	def getStrategyCounts(self):
		"""Return a list where each element represents the strategyID of an agent"""

		populationSize = self.config['size']
		propOfStrategies = self.config['distribution']
		countsOfStrategies = [int(val*populationSize) for val in propOfStrategies]
		pop = []
		for i in range(len(countsOfStrategies)):
			for _ in range(countsOfStrategies[i]):
				pop.append(i)
		return pop
	
	def getCensus(self):
		"""Return a dictionary where the key-value pairs are the strategy IDs and the number of agents running that strategy."""
		censusCopy = copy.deepcopy(Strategy.census)
		return censusCopy

	def getCensusProportions(self):
		"""Return a dictionary where the key-value pairs are the strategy IDs and the proportion of the population running that strategy."""

		census = self.getCensus()
		size = self.config['size']
		for key, _ in census.items():
			census[key] /= size
		return census

	def createNetwork(self, agentType):
		"""Generate an Erdos-Renyi random graph with density as specified in the configuration class (configBuilder)."""
		#TODO: Check Erdos Renyi, think I am iterating through each edge TWICE -> doubling the density of the random graph - https://stackoverflow.com/questions/31079526/how-to-iterate-over-each-edge-of-a-complete-graph-exactly-once

		strategyDistribution = self.getStrategyCounts()

		for agentID in range(self.config['size']):
			randomStrategyIndex = random.randint(0, len(strategyDistribution)-1)
			self.agentList.append(agentType(_id=agentID, _strategy=strategyDistribution[randomStrategyIndex]))
			strategyDistribution.pop(randomStrategyIndex)
			self.population.add_node(self.agentList[agentID])

		for agentID1 in range(len(self.population)):
			for agentID2 in range(agentID1+1, len(self.population)):
				if agentID1 != agentID2:
					r = random.random()
					if r < self.config['density']:
						self.population.add_edge(self.agentList[agentID1], self.agentList[agentID2])
						if self.agentList[agentID2] not in self.agentList[agentID1].neighbours:
							self.agentList[agentID1].neighbours.append(self.agentList[agentID2])
						if self.agentList[agentID1] not in self.agentList[agentID2].neighbours:
							self.agentList[agentID2].neighbours.append(self.agentList[agentID1])

		self.__initialiseAgentHistories()

	def getOpponentsReputation(self, agent1, agent2):
		"""Must be implemented through the relevent network type. Can be Global or Local."""
		raise NotImplementedError

	def updateMonitor(self, agent1, agent2, payoff1, payoff2):
		agent1ID = agent1.currentStrategy.currentStrategyID
		agent2ID = agent2.currentStrategy.currentStrategyID
		self.utilityMonitor[0][agent1ID] += 1
		self.utilityMonitor[1][agent1ID] += payoff1
		self.utilityMonitor[0][agent2ID] += 1
		self.utilityMonitor[1][agent2ID] += payoff2

	def playSocialDilemna(self):

		# Two agents chosen randomly from the population
		agent1, agent2 = self.chooseTwoAgents()
		agent1Reputation, agent2Reputation = self.getOpponentsReputation(agent1, agent2)

		# Each agent calculates their move according to their behavioural strategy
		agent1Move = agent1.currentStrategy.chooseAction(agent1.currentReputation, agent2Reputation)
		agent2Move = agent2.currentStrategy.chooseAction(agent2.currentReputation, agent1Reputation)
		self.tempActions[agent1Move] += 1
		self.tempActions[agent2Move] += 1
		
		# Calculate each agent's payoff
		payoff1, payoff2 = self.dilemna.playGame(agent1Move, agent2Move)
		self.updateMonitor(agent1, agent2, payoff1, payoff2)

		# Update agents personal utilities for evolutionary update
		agent1.updateUtility(payoff1)
		agent2.updateUtility(payoff2)

		self.updateInteractions(agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move)
		self.updateReputation(agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move)


	def resetUtility(self):
		"""Reset the utility of each agent in the population. To be used at the end of every timestep."""
		for agent in self.agentList:
			agent.currentUtility = 0
		self.utilityMonitor = [{}.fromkeys(range(10), 0), {}.fromkeys(range(10), 0)]


	def updateInteractions(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
		interaction12 = {
			'Opponent': agent2,
			'Focal Reputation': agent1.currentReputation,
			'Opponent Reputation': agent2Reputation,
			'Focal Move': agent1Move,
			'Opponent Move': agent2Move
		}
		agent1.recordInteraction(interaction12)
		interaction21 = {
			'Opponent': agent1,
			'Focal Reputation': agent2.currentReputation,
			'Opponent Reputation': agent1Reputation,
			'Focal Move': agent2Move,
			'Opponent Move': agent1Move
		}
		agent2.recordInteraction(interaction21)

	def updateReputation(self, agent1, agent2, agent1Reputation, agent2Reputation, agent1Move, agent2Move):
		"""Assign reputations following an interaction with each agent's globally known reputation and not the calculated reputation as default."""

		agent1NewReputation = self.socialNorm.assignReputation(agent1.currentReputation, agent2.currentReputation, agent1Move)
		agent2NewReputation = self.socialNorm.assignReputation(agent2.currentReputation, agent1.currentReputation, agent2Move)

		agent1.updatePersonalReputation(agent1NewReputation)
		agent2.updatePersonalReputation(agent2NewReputation)

	def showHistory(self):
		for agent in self.agentList:
			s = f"History for agent {agent.id} \n"
			s += agent.getHistory()
			s += "\n"
			print(s)

	def checkConvergence(self):
		"""Check if the network has converged or not by checking the last 3 snapshots taken at randomly chosen intervals."""
		
		history = self.convergenceHistory

		# Minimum 3 snapshots needed to check for convergence (as defined in self.convergenceHistory)
		if None in history:
			return

		if history[2] == history[1] and history[1] == history[0]:
			self.hasConverged = True
			self.results.convergedAt = self.currentPeriod

	def chooseTwoAgents(self):
		agent1 = random.choice(self.agentList)
		agent2 = random.choice(self.agentList)
		while agent2 == agent1:
			agent2 = random.choice(self.agentList)
		return (agent1, agent2)

	def mutation(self, mutantStrategyID):
		"""Each agent has probability of () 1/n )/alpha of becoming an agent in any time period where alpha is a parameter > 1"""
		probabilityOfMutation = 1/(self.config['size']*self.config['probabilityOfMutants'])
		for agent in self.agentList:
			r = random.random()
			if r < probabilityOfMutation:
				agent.currentStrategy.changeStrategy(mutantStrategyID)
		

	def evolutionaryUpdate(self, alpha=10):
		"""Must be implemented through the relevent network type."""
		raise NotImplementedError


	def runSingleTimestep(self):
		"""Run one single time-step with multiple interactions between randomly selected agents"""
		self.playSocialDilemna()
		r = random.random()
		while r < self.config['omega']:
			self.playSocialDilemna()
			r = random.random()
		
		self.results.updateActions(self.tempActions)

	def grabSnapshot(self):
		self.convergenceHistory.appendleft(self.getCensus())

	def __initialiseAgentHistories(self):
		for agent in self.agentList:
			agent.initialiseHistory()

	def __getStrategyColours(self):
		colourMap = []
		for agent in self.agentList:
			colourMap.append(agent.colour)
		return colourMap

	def __str__(self):
		s = ""
		for agent in self.agentList:
			s += str(agent) + "\n"
		return s


if __name__ == "__main__":
	pass


