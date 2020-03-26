class Results:

    def __init__(self, config):
        self.strategies = {config.population.ID, config.mutant.ID}
        self.actions = {'C': [], 'D': []}
        self.strategyProportions = {}
        self.utilities = {}
        self.convergedAt = None
        self.mutantTracker = {}

