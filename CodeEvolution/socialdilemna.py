class SocialDilemna():

	def __init__(self):
		pass

	def playGame(self, agent1Action, agent2Action):
		agent1Payoff = self.payoff1[agent1Action][agent2Action]
		agent2Payoff = self.payoff2[agent1Action][agent2Action]
		return [agent1Payoff, agent2Payoff]

class PrisonersDilemna(SocialDilemna):

	def __init__(self, benefit, cost):
		SocialDilemna.__init__(self)
		self.payoff1 = {
			'C': {
				'C': benefit-cost,
				'D': -cost
			},
			'D': {
				'C': benefit,
				'D': 0
			}
		}
		self.payoff2 = {
			'C': {
				'C': benefit-cost,
				'D': benefit
			},
			'D': {
				'C': -cost,
				'D': 0
			}
		}


def main():
	S = PrisonersDilemna(2, 1)
	payoffs = S.playGame('C', 'C')
	print(payoffs)

if __name__=='__main__':
	main()
