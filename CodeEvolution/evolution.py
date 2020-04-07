import copy
import logging
import random


class GlobalEvolution:
    """This class supplies the global evolutionary mechanisms to any subclass that inherits from it. This class should
    not be directly instantiated."""

    def evolutionaryUpdate(self):
        """Global Evolution - Find the strategy with the highest utility and the proportion of the utility over the
         utilities of all strategies."""

        strategyUtils = copy.deepcopy(
            self.results.utilities[self.currentPeriod])
        logging.debug(f"\tStrategyUtils: {strategyUtils}")

        # find strategy with highest utility
        bestStrategy = max(strategyUtils, key=lambda key: strategyUtils[key])

        # check for strategies with negative utility
        # for strategy, utility in strategyUtils.items():
        #     if utility < 0:
        #         strategyUtils[strategy] = 0

        # if total utility is zero, no evolutionary update
        # totalUtil = sum(strategyUtils.values())
        # if totalUtil == 0:
        #     logging.debug(
        #         f"\tupdate skipped because we have {strategyUtils.values()}")
        #     return

        # probability of switching to strategy i is (utility of strategy i)/(total utility of all non-negative
        # strategies)*(speed of evolution, larger the alpha, the slower the evolution)
        # for strategy, _ in strategyUtils.items():
        #     # strategyUtils[strategy] /= (totalUtil * alpha)
        #     # strategyUtils[strategy] /= (totalUtil * 10)
        #     strategyUtils[strategy] /= (totalUtil * self.config.size)
        # print(strategyUtils)
        # logging.debug(
        #     f"\tt = {self.currentPeriod}, probabilities are {strategyUtils}, best strategy is {bestStrategy}")

        for agent in self.agentList:
            if random.random() < self.config.alpha:
                logging.debug(
                    f"Agent {agent.id} switched from {agent.Strategy.ID} to {bestStrategy}")
                agent.Strategy.changeStrategy(bestStrategy)


class LocalEvolution:
    """This class supplies the local evolutionary mechanisms to any subclass that inherits from it. This class should
    not be directly instantiated."""

    def findBestLocalStrategy(self, copyTheBest=None):
        """Find the strategy of your best/better performing neighbour. If there are multiple, choose randomly of the
         strategies with maximum utility.

        Args:
            copyTheBest (bool): If True, the focal agent will only consider updating to the best strategy in his
                neighbourhood, otherwise if False, he may choose to update to any strategy better than his own.

        Returns:
            The strategy ID of the agent with the greatest utility out of the immediate neighbourhood.
        """

        neighbourUtilities = list(
            map(lambda x: x.currentUtility, self.neighbours))
        if copyTheBest:
            # Find the strategy locally that is performing the best
            maxLocalUtility = max(neighbourUtilities)
            indices = [i for i, x in enumerate(
                neighbourUtilities) if x == maxLocalUtility]
        else:
            # Find all the strategies from the neighbouring agent's who are fairing better than the focal agent
            betterLocalUtilities = [
                util for util in neighbourUtilities if util > self.currentUtility]
            indices = [i for i, x in enumerate(
                neighbourUtilities) if x == random.choice(betterLocalUtilities)]

        # Choose randomly from shortlisted agents
        bestLocalStrategyID = random.choice(indices)

        return self.neighbours[bestLocalStrategyID].Strategy.ID

    def evolutionaryUpdate(self):
        """Local Learning - Out of the subset of agents that are connected to the focal agent, adopt the strategy of the
         best/better performing agent with some probability."""

        # Find each agent's new strategy
        strategy_mapping = {}.fromkeys(self.agentList)
        for agent in self.agentList:
            if random.random() < self.config.alpha:
                # Update strategy
                strategy_mapping[agent] = agent.findBestLocalStrategy(copyTheBest=True)
            else:
                # Stick with same strategy
                strategy_mapping[agent] = agent.Strategy.ID

        # Agent's actually change their strategy
        for agent in strategy_mapping.keys():
            if agent.Strategy.ID == strategy_mapping[agent]:
                continue
            else:
                agent.Strategy.changeStrategy(strategy_mapping[agent])



