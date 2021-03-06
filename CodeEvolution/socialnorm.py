class SocialNorm():
    allStates = ['11C', '11D', '10C', '10D', '01C', '01D', '00C', '00D']
    allOutcomes = [[1, 0, 1, 1, 1, 0, 1, 0],
                   [1, 0, 0, 1, 1, 0, 1, 0],
                   [1, 0, 1, 1, 1, 0, 1, 1],
                   [1, 0, 1, 1, 1, 0, 0, 1],
                   [1, 0, 0, 1, 1, 0, 1, 1],
                   [1, 0, 0, 1, 1, 0, 0, 1],
                   [1, 0, 1, 1, 1, 0, 0, 0],
                   [1, 0, 0, 1, 1, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

    def __init__(self, _stateID):
        self.states = dict((key, value) for key, value in zip(self.allStates, self.allOutcomes[_stateID]))
        self.stateID = _stateID

    def assignReputation(self, agent1Reputation, agent2Reputation, agent1Action):
        """Return agent1's new reputation given his and his opponent's current reputation and agent1's action"""
        state_key = str(agent1Reputation) + str(agent2Reputation) + str(agent1Action)
        return self.states[state_key]

    def __str__(self):
        return str(self.states)


if __name__ == "__main__":
    pass
