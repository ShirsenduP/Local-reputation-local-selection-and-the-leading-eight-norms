import copy
import logging
import random


class GlobalEvolution:
    """This class supplies the global evolutionary mechanisms to any subclass that inherits from it. This class should
    not be directly instantiated."""

    def evolutionaryUpdate(self, alpha=10):
        """Global Evolution - Find the strategy with the highest utility and the proportion of the utility over the
         utilities of all strategies."""

        strategyUtils = copy.deepcopy(
            self.results.utilities[self.currentPeriod])
        logging.debug(f"\tStrategyUtils: {strategyUtils}")

        # find strategy with highest utility
        bestStrategy = max(strategyUtils, key=lambda key: strategyUtils[key])

        # check for strategies with negative utility
        for strategy, utility in strategyUtils.items():
            if utility < 0:
                strategyUtils[strategy] = 0

        # if total utility is zero, no evolutionary update
        totalUtil = sum(strategyUtils.values())
        if totalUtil == 0:
            logging.debug(
                f"\tupdate skipped because we have {strategyUtils.values()}")
            return

        # probability of switching to strategy i is (utility of strategy i)/(total utility of all non-negative
        # strategies)*(speed of evolution, larger the alpha, the slower the evolution)
        for strategy, _ in strategyUtils.items():
            strategyUtils[strategy] /= (totalUtil * alpha)

        logging.debug(
            f"\tt = {self.currentPeriod}, probabilities are {strategyUtils}, best strategy is {bestStrategy}")

        for agent in self.agentList:
            r = random.random()
            if r < strategyUtils[bestStrategy]:
                logging.debug(
                    f"Agent {agent.id} switched from {agent.Strategy.ID} to {bestStrategy}")
                agent.Strategy.changeStrategy(bestStrategy)


class LocalEvolution:
    """This class supplies the local evolutionary mechanisms to any subclass that inherits from it. This class should
    not be directly instantiated."""

    def evolutionaryUpdate(self, alpha=10):
        """Local Learning - Out of the subset of agents that are connected to the focal agent, adopt the strategy of the
         best/better performing agent with some probability."""
        # WARN: BUG? Anyone who is yet to update, but is connected to an already updated agent has a chance of updating
        #  with incorrect information, primarily the original strategies of all his neighbouring agents before
        #  update. Don't think this affects primary results, but only the speed of evolution, can accellerate the
        #  speed of evolution of a profitable strategy

        # Find each agent's new strategy
        strategy_mapping = {}.fromkeys(self.agentList)
        for agent in self.agentList:
            if random.random() < self.config.updateProbability:
                strategy_mapping[agent] = agent.findBestLocalStrategy(copyTheBest=True)

        # Agent's actually change their strategy
        for agent in strategy_mapping.keys():
            if agent.Strategy.ID == strategy_mapping[agent]:
                continue
            else:
                agent.Strategy.changeStrategy(strategy_mapping[agent])



