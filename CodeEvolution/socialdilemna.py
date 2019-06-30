class SocialDilemna():
    """Parent class of all social dilemna games that can be played in this experiment, providing the means through which each game outputs the respective payoffs of either side of the game."""

    def __init__(self):
        pass

    def playGame(self, agent1Action, agent2Action):
        if agent1Action not in ['C', 'D'] or agent2Action not in ['C', 'D']:
            raise ValueError("Agent move is not valid ('C' or 'D')")

        agent1Payoff = self.payoff1[agent1Action][agent2Action]
        agent2Payoff = self.payoff2[agent1Action][agent2Action]
        return [agent1Payoff, agent2Payoff]

class PrisonersDilemna(SocialDilemna):
    """Prisoner's Dilemna game parameterised by a benefit and a cost, the benefit is received by agent1 if agent2 cooperates with them, and the cost is paid by agent1 if it cooperates with agent2."""
    
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
    pass


if __name__=='__main__':
    main()
