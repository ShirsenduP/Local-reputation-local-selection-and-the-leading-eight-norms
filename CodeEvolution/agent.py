import random

from CodeEvolution.strategy import Strategy

class Agent():

    reputation = (0,1)
    strategyColour = {
        0: "orange", 
        1: "tan",
        2: "palegreen",
        3: "turquoise",
        4: "cornflowerblue",
        5: "royalblue",
        6: "plum",
        7: "lightpink",
        8: "black",
        9: "green"
    }

    def __init__(self, _id, _strategy):
        self.id = _id
        self.currentStrategy = Strategy(_strategy)
        self.currentReputation = random.choice(Agent.reputation)
        self.currentUtility = 0
        self.neighbours = []
        self.history = {} # get LAST partner
        self.colour = self.strategyColour[self.currentStrategy.currentStrategyID]

    def updateUtility(self, payoff):
        """Update the utility or cumulative payoff of an agent."""
        self.currentUtility += payoff

    def findBestLocalStrategy(self, copyTheBest):
        """Find the strategy of your best/better performing neighbour. If there are multiple, choose randomly of the strategies with maximum utility."""
        neighbourUtilities = list(map(lambda x:x.currentUtility, self.neighbours))
        if copyTheBest:
            maxLocalUtility = max(neighbourUtilities)
            indices = [i for i, x in enumerate(neighbourUtilities) if x == maxLocalUtility]
        else:
            betterLocalUtilities = [util for util in neighbourUtilities if util > self.currentUtility]
            indices = [i for i, x in enumerate(neighbourUtilities) if x == random.choice(betterLocalUtilities)]
        bestLocalStrategyID = random.choice(indices)

        return self.neighbours[bestLocalStrategyID].currentStrategy.currentStrategyID
        
    def updateStrategy(self, updateProbability, copyTheBest=True):
        """(COPY THE BEST) Switch strategies to the strategy used by the best performing neighbour of the agent with some probability."""
        r = random.random()
        if r < updateProbability:
            newStrategyID = self.findBestLocalStrategy(copyTheBest)
            if newStrategyID == self.currentStrategy.currentStrategyID:
                return
            self.currentStrategy.changeStrategy(newStrategyID)

    
        # TODO: Replicator dyamics (in model_experiment.pdf)
            
    def updatePersonalReputation(self, newRep):
        """Update own reputation, only to be used for an agent's own reputation from their point of view in an interaction."""
        self.currentReputation = newRep

    def summary(self):
        # s = "Summary of Network\n"
        s = f"Agent {self.id} is currently running strategy {self.currentStrategy} with current reputation {self.currentReputation}"
        return s

    def initialiseHistory(self):
        """Only keep track of interactions with your neighbours."""
        self.history = {}.fromkeys(self.neighbours)

    def recordInteraction(self, interaction):
        """Remember the previous interaction with your neighbours (and no one else)."""
        if interaction['Opponent'] in self.neighbours:
            self.history[interaction['Opponent']] = interaction

    def getHistory(self):
        s = ""
        for neighbour in self.neighbours:
            s += f"Last interaction with neighbour {neighbour.id} was {self.history[neighbour]}\n"
        return s

    def __str__(self):
        s = "("
        s += f"Agent {self.id}"
        s += f"# of agents {len(self.neighbours)}"
        s += f", s={self.currentStrategy.currentStrategyID}"
        return s

if __name__ == "__main__":
    pass






