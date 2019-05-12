class SocialDilemna():

	def __init__(self):
		self.payoff = []
7
	def playGame(self, agent1Action, agent2Action):
		# return payoffs to agent 1 and agent 2
		# assign new reputations using social norms
		pass


class PrisonersDilemna(SocialDilemna):

	def __init__(self):
		SocialDilemna.__init__(self)





S = PrisonersDilemna()

print(S.payoff)














"""
TODO:

1	Generalise prisoners dilemna to  social dilemna class, so it can be easily chosen/swapped out for another and easily modified
2	ALTERNATIVE to 1, have a class variable: dictionary of all social dilemnas


"""