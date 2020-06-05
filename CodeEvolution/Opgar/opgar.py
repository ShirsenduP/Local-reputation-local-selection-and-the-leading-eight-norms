"""

"""

import copy
import logging
import random
from datetime import datetime
from random import choice, shuffle

import numpy as np
import pandas as pd
import yaml


def format_long():
    """Show pandas dataframes in full."""
    import pandas
    pandas.set_option("display.max_rows", None)
    pandas.set_option("display.max_columns", None)
    pandas.set_option("display.width", None)


class Configuration:
    """Provides the functionality and error checking for all parameterizations of simulations."""

    __slots__ = ["social_norm", "composition", "t", "k", "m", "N"]

    def __init__(self, population_size: int, pgg_size: int, technology: float, rounds: int, composition: dict,
                 norm: str):
        """

        Args:
            population_size (int): The number of players in the population.
            pgg_size (int): The number of players per Public Goods Game (PGG).
            rounds (int): The length of the simulation.
            technology (float): The growth factor to the group contribution in the PGG.
            composition (dict): A dictionary of strategy and proportion key-value pairs. See _Strategy documentation.
            norm (str): The specific social norm within the population. See _Norm documentation.
        """

        if norm not in _Norm.social_norm_names:
            raise ValueError(f"Your choice of norm ('{norm}') is invalid.")
        self.social_norm = norm

        if sum(composition.values()) != 1:
            raise ValueError(
                f"Your choice of strategy proportions must sum to 1 (not '{sum(composition.values())}').")
        for strategy in composition.keys():
            if strategy not in _Strategy.names:
                raise ValueError(f"Your choice of strategy ('{strategy}') is invalid.")
            if composition[strategy] < 0 or composition[strategy] > 1:
                raise ValueError(
                    f"Your choice of strategy proportion ('{strategy}': {composition[strategy]}) is invalid.")
        self.composition = composition

        if rounds < 1:
            raise ValueError(f"Your choice of rounds ('{rounds}') is invalid.")
        self.t = rounds

        if technology < 1:
            raise ValueError(f"Your choice of technology ('{technology}') is invalid.")
        self.k = technology

        if population_size < 0:
            raise ValueError(f"Your choice of population size ('{population_size}') is invalid.")
        self.N = population_size

        if pgg_size < 0 or pgg_size > population_size:
            raise ValueError(f"Your choice of PGG size ('{pgg_size}') is invalid.")
        if not population_size % pgg_size == 0:
            raise ValueError(
                f"The PGG size ('{pgg_size}') must be a divisor of the population size ('{population_size}').")
        self.m = pgg_size

    def __repr__(self):
        return f"Configuration(population_size={self.N}, pgg_size={self.m}, technology={self.k}, rounds={self.t}, composition={self.composition}, norm={self.social_norm})"


class _Strategy:
    """
    The _Strategy class provides all the relevant behavioural strategy functions for agents deciding their actions.

    - Strategy names can be listed by calling _Strategy.names
    - _Strategy.choices is a dictionary of strategy: function pairs
    - _Strategy.description provides the written rule of the strategy

    To choose an action for an agent, call _Strategy.choose_action(ID) where ID is any string in _Strategy.names
    """
    names = ["I",
             "II",
             "III",
             "IV",
             "V",
             "VI",
             "VII",
             "VIII",
             "IX",
             "X",
             "XI"]

    choices = {
        "I": lambda avg: 1,
        "II": lambda avg: 0,
        "III": lambda avg: None,
        "IV": lambda avg: 1 if avg > -1 else 0,
        "V": lambda avg: 1 if avg > 0 else 0,
        "VI": lambda avg: 1 if avg > -1 else None,
        "VII": lambda avg: 1 if avg > 0 else None,
        "VIII": lambda avg: 0 if avg > -1 else None,
        "IX": lambda avg: 0 if avg > 0 else None,
        "X": lambda avg: None if avg > -1 else 0,
        "XI": lambda avg: None if avg > 0 else 0
    }

    descriptions = {
        "I": "Unconditional Cooperation",
        "II": "Unconditional Defection",
        "III": "Never participate",
        "IV": "Cooperate if anyone in the group is not bad otherwise defect",
        "V": "Cooperate if group has mostly good people otherwise defect",
        "VI": "Cooperate if anyone in the group is not bad otherwise don't participate",
        "VII": "Cooperate if group has mostly good people otherwise don't participate",
        "VIII": "Defect if group has any not-bad people otherwise don't participate",
        "IX": "Defect if group is mostly good otherwise don't participate",
        "X": "Don't participate if group has anyone not-bad otherwise defect",
        "XI": "Don't participate if group is mostly good otherwise defect"
    }

    @staticmethod
    def choose_action(ID):
        """
        Return a function implementing the agent's behavioural strategy depending on the strategy from _Strategy.names.
        Each agent stores a reference to their function in _Strategy.choices to call as needed.

        Args:
            ID (str): A string representation the 11 behavioural strategies 'I' - 'XI' within the model
        Returns:
            _Strategy.choices[ID] (func): A function requiring a single argument 'average reputation'. See
            agent.choose_action for more information.
        """
        return _Strategy.choices[ID]


class _Norm:
    """
    A population-wide object specifying the rules of reputation assignment after a round of the Public Goods Game.

    Use _Norm.social_norm_names fpr a list of the social norm names
    Use _Norm.social_norm_rules for the dictionary of actions: reputation pairs
    Use _Norm.social_norm_descriptions for an explanation of each norm

    Args:
        norm_name (str) = Name of the social norm of the population, can be one of ["Loner", "Defector", "Neither", \
        None].
    """
    social_norm_names = [
        "Loner",
        "Defector",
        "Neither",
        None
    ]

    social_norm_rules = {
        "Loner": {
            1: 1,
            0: 0,
            None: -1
        },
        "Defector": {
            1: 1,
            0: -1,
            None: 0
        },
        "Neither": {
            1: 1,
            0: 0,
            None: 0
        },
        None: None
    }

    social_norm_descriptions = {
        "Loner": {
            "Name": "Loner",
            "Summary": "This is the social norm that is biased against people who do not contribute.",
            "Rule": "Assign 1 (good) if player contributed, 0 (okay) if he defected, -1 (bad) if he did not "
                    "participate.",
        },
        "Defector": {
            "Name": "Defector",
            "Summary": "This is the social norm that is biased against people who participate but do not contribute.",
            "Rule": "Assign 1 (good) if player contributed, 0 (okay) if he didn't participate, -1 (bad) if he "
                    "participated but did not contribute.",
        },
        "Neither": {
            "Name": "Neither",
            "Summary": "This is the social norm that is indifferent towards Loners or Defectors.",
            "Rule": "Assign 1 (good) if player contributed, 0 (okay) if he did not contributed or if he did not "
                    "participate.",
        },
        None: {
            "Name": "None",
            "Summary": "This is the social norm that ignores reputation.",
            "Rule": "No actions are assigned reputations. This is only valid in populations with only strategies "
                    "I, II, and III. Errors will be raised to prevent this.",
        }
    }

    def __init__(self, norm_name):
        self.norm_name = norm_name
        self.reputation_matrix = _Norm.social_norm_rules[norm_name]

    def assign_reputation(self, contribution):
        """
        Given a contribution, assign new reputations according to the social norm type
        Args:
            contribution (int or None): An agent's contribution (1) or defection (0) or loner (None)

        Returns:
            A new reputation, either good (1), okay (0), bad (-1)
        """
        return self.reputation_matrix[contribution]


class _Agent:

    def __init__(self, ID, strategy):
        self.ID = ID
        self.strategy = strategy
        self.utility = 1
        self.reputation = [choice([-1, 0, 1])]
        self.tracker = []

    def choose_action(self, average_reputation):
        """
        _Agent chooses it's action in a public good game given the average reputation of the other players. Choice
        depends on the player's strategy.
        Args:
            average_reputation (float): The average reputation in [-1, 1] of the other players in the group

        Returns:
            Action (str): Contributes 1 or 0 if playing, if not participating, then return None
        """
        return _Strategy.choose_action(self.strategy)(average_reputation)


class Population:
    """Simulate a population of agents playing public goods games.

    Generate a population of N agents* to play the Public Good Game in groups* of m. Each agent is initialised with
    utility 1 and a behavioural strategy*.

    * As declared in the config dictionary

    Examples:
        Define a dictionary containing all the parameters for a single simulation. Create a Population object using
        the parameter dictionary. Run the simulation.

        >>> C = { \
                "N": 1000, \
                "m": 4, \
                "k": 2, \
                "t": 30, \
                "composition": {"I": 1 / 3, "II": 1 / 3, "III": 1 / 3}, \
                "social_norm": "Defector", \
                }
        >>> P = Population(C)
        >>> df = P.simulate()

    """

    def __init__(self, config):
        """
        Create a Population object ready to start simulating.

        Args:
            config (opgar.Configuration): Object of simulation parameters.
        """

        self.config = config
        self.strategies = list(config.composition.keys())

        # Generate agents with strategy distribution
        self.agents = self._generate_population(config.N, config.composition)
        self.social_norm_type = config.social_norm
        self.social_norm = _Norm(config.social_norm)

    def simulate(self):
        """
        Simulate multiple rounds of public goods games
        Returns:
            Pandas DataFrame of simulation results
        """
        all_results = {}.fromkeys(range(self.config.t))
        for t in range(self.config.t):
            all_results[t] = self._play_public_good_game()
            if self.social_norm_type:
                self._update_reputations()
            self._evolve(all_results[t])
            self._reset_population()
        all_results = pd.concat(all_results.values(), axis=1, ignore_index=True).transpose()
        all_results.index.name = "T"
        return all_results

    def _update_reputations(self):
        """
        Iterate through the population and update their reputations based on the social norm and their previous action.
        """
        # If we don't care about reputation
        if self.social_norm is None:
            return

        for agent in self.agents:
            most_recent_action = agent.tracker[-1]
            current_reputation = agent.reputation
            new_reputation = self.social_norm.assign_reputation(most_recent_action)
            agent.reputation.append(new_reputation)
            logging.debug(f"A{agent.ID}(old_reputation={current_reputation}, new_reputation={new_reputation}")

    def _play_public_good_game(self):
        """
        Simulate the public good game (PGG) once for each player in the population

        Returns: Pandas DataFrame containing the outcome of the single round of PGG. Data includes population
        composition and total/average payoffs by strategy

        """

        # Setup time-step
        time_step_result = {
            "Payoffs": {}.fromkeys(self.strategies, 0),
            "Composition Count": {}.fromkeys(self.strategies, 0),
            "Composition": {}.fromkeys(self.strategies, 0),
            "Average Payoffs": {}.fromkeys(self.strategies, 0),
        }

        # Randomly allocate groups
        player_IDs = np.arange(self.config.N)
        shuffle(player_IDs)
        groups_of_player_IDs = np.reshape(player_IDs, (int(self.config.N / self.config.m), self.config.m))

        for group in groups_of_player_IDs:
            avg_rep = sum([self.agents[ID].reputation[-1] for ID in group]) / self.config.m
            group_contribution = 0
            absent_players_IDs = list()

            for playerID in group:
                # Players decide to contribute 1, contribute 0, or not participate
                contribution = self.agents[playerID].choose_action(average_reputation=avg_rep)
                self.agents[playerID].tracker.append(contribution)

                # Player does not participate
                if contribution is None:
                    absent_players_IDs.append(playerID)
                    continue

                # Player participates
                self.agents[playerID].utility -= contribution
                group_contribution += contribution

            # If there is 1 or less player *participating*, PGG is not played
            participating_agents_count = self.config.m - len(absent_players_IDs)
            if participating_agents_count < 2:
                # TODO: logging required here? Need to research good logging processes
                continue

            # Create payoff per participating agent within the group
            game_payoff = (self.config.k * group_contribution) / participating_agents_count

            # Distribute payoffs
            for playerID in group:
                if playerID in absent_players_IDs:
                    continue
                self.agents[playerID].utility += game_payoff

        # Record total strategy payoffs, strategy composition
        for agent in self.agents:
            time_step_result["Payoffs"][agent.strategy] += agent.utility
            time_step_result["Composition Count"][agent.strategy] += 1

        for strategy in self.strategies:
            # If no players left in the strategy, payoff is 0
            player_count = time_step_result["Composition Count"][strategy]
            if player_count == 0:
                time_step_result["Average Payoffs"][strategy] = 0
                continue

            # Average strategy payoffs by number of agents using the strategy
            time_step_result["Average Payoffs"][strategy] = time_step_result["Payoffs"][strategy] / player_count

            # Get population composition as a proportion instead of relative size
            time_step_result["Composition"][strategy] = time_step_result["Composition Count"][strategy] / self.config.N

        # Convert to sets
        reform = {(outerKey, innerKey): values for outerKey, innerDict in time_step_result.items() for innerKey, values
                  in
                  innerDict.items()}
        df = pd.Series(reform)
        return df

    def _evolve(self, result):
        """
        Using a replicator equation, update the population strategy composition.

        Using the average payoffs per strategy in the most recent time-step, calculate the new proportions of each
        strategy within the population by the following steps:
            1) Get products of the proportions of the strategies and their corresponding average payoff.
            2) Sum all of the products in 1) to get the population fitness
            3) The new proportion of strategy S is calculated by:
                S(t+1) = S(t) + S(t) * ( AvgPayoff(S) - PopulationFitness )
            4) The new population composition is multiplied by the population size and the numbers are adjusted to
                integer equivalents by the largest remainder method.
            5) Randomly select an agent from the population and change them if their strategy needs either more/less
                agents until the new population state/composition is reached.

        Args:
            result (pandas.DataFrame): Set of results from a single time-step (should be the most recent one), used to
            calculate the new proportion of the strategies within the population using the replicator equation.
        """
        # Get Average payoff for each stratagy
        payoffs = result["Average Payoffs"]
        # Get population state of each strategy
        compositions = result["Composition"]

        # Average fitness over entire population
        average_fitness = payoffs * compositions
        average_fitness = average_fitness.sum()

        # Get new population state
        new_comp = {}
        for strategy in self.strategies:
            new_comp[strategy] = float(
                compositions[strategy] + compositions[strategy] * (payoffs[strategy] - average_fitness))
        new_composition_proportion_rounded = Population._round_to_n_percent(new_comp,
                                                                            self.config.N)

        composition_change = new_composition_proportion_rounded - result["Composition Count"]
        while composition_change.abs().sum() != 0:

            # Pick a random agent from the population
            random_agent = self.agents[choice(range(self.config.N))]
            random_agent_strategy = random_agent.strategy

            # Check if this agent's strategy needs less players
            if composition_change[random_agent_strategy] < 0:
                # strategies = list(composition_change.keys())
                # new_strategy = strategies[changes.index(max(changes))]
                new_strategy = composition_change.idxmax()

                # new_strategy = composition_change[composition_change == max(composition_change)].index[0]
                random_agent.strategy = new_strategy
                composition_change[random_agent_strategy] += 1
                composition_change[new_strategy] -= 1
                logging.debug(f"A({random_agent.ID}) switched from strategy {random_agent_strategy} to {new_strategy}")

    def _reset_population(self):
        """
        Reset all agents and the population between time-steps.

        Things that are reset:
            An agent's utility is reset to 1

        Things that do not reset:
            An agent's reputation
            Any population parameters

        """
        for agent in self.agents:
            agent.utility = 1

    @staticmethod
    def _generate_population(N, composition):
        """
        Create the population of agents with the required distribution of strategies.

        Given some proportion of strategies within the population as a dictionary of strategy: 'proportion of 1' pairs,
        convert the proportions to numbers of agents by multiplying by the size of the population. These may or may not
        be non-integers, so we use the Largest Remainder method to assign the last few agents.

        Args:
            N (int): Size of the network
            composition (dict): Dictionary of strategies and their proportions within the population

        Returns:
            List of agents with a strategy distribution equal to that of composition
        """

        proportions = Population._round_to_n_percent(composition, N)

        agents = []
        id_counter = 0
        for strategy, count in proportions.items():
            for _ in range(int(count)):
                agents.append(_Agent(ID=id_counter, strategy=strategy))
                id_counter += 1

        return agents

    @staticmethod
    def _is_valid(config):
        """
        Check the below conditions for simulation.
            1) N is a multiple of PGG group size m
            2) composition sums to 1
            3) N, m, k, t must be positive
            4) composition proportions must be positive
            5) Norm=None is not combined with strategies that require a social norm
        Args:
            config (dict): Configuration dictionary containing simulation parameters

        Returns:
            True if valid, else an error code corresponding to the above cases
        """

        # 1)
        population_divisible_by_group_size = config['N'] % config['m']
        if population_divisible_by_group_size != 0:
            return 1, f"Group Size is {population_divisible_by_group_size}"

        # 2)
        sum_of_compositions = round(sum(config['composition'].values()), 10)
        if sum_of_compositions != 1:
            return 2, f"Sum of population composition is {sum_of_compositions}"

        # 3)
        positive_keys = ["N", "m", "k", "t"]
        for key in positive_keys:
            if config[key] < 0:
                return 3, f"{key} is {config[key]}"

        # 4)
        for prop in config['composition'].values():
            if prop < 0:
                return 4, f"{prop} cannot be negative"

        # 5)
        # If social norm is not explicitly stated, then reputation is ignored
        acceptable_strategies_with_no_norm = set(_Strategy.names[:3])
        if "social_norm" not in config:
            if not set(config["composition"].keys()).union(acceptable_strategies_with_no_norm):
                raise Exception("A social norm is not specified but the current strategies will need one.")
            config["social_norm"] = None

        # If social norm is None, check there are no strategies that require one
        if config["social_norm"] == None:
            for strategy in config["composition"].keys():
                if strategy not in acceptable_strategies_with_no_norm:
                    return 5, f"Strategy {strategy} cannot be in a population with no social norm."

        # 6)
        # N and m must be greater than 4
        if config["N"] < 4:
            return 6, f"Population cannot have less than 4 agents (here it is {config['N']})"
        if config["m"] < 4:
            return 6, f"PGG group size cannot be less than 4 agents (here it is {config['m']})"

        return 0, None

    @staticmethod
    def _round_to_n_percent(number_set, n):
        """
        Modified from https://stackoverflow.com/questions/25271388/python-percentage-rounding

        This function take a list of number and return a list of percentage, which represents the portion of each number in sum of all numbers
        Moreover, those percentages are adding up to 100%!!!
        Notice: the algorithm we are using here is 'Largest Remainder'
        The down-side is that the results won't be accurate, but they are never accurate anyway:)

        Args:
            number_set (dict): A mapping of classes to proportions of 1
            n (int): The size of the population the proportions need to be mapped to

        Examples:
            # TODO: Create some examples with the general and edge cases (AFTER CONVERTING TO PANDAS.SERIES)
        """
        total = float(sum(number_set.values()))
        # TODO: Change this from using dictionaries to pandas.Series
        unround_numbers = {x: n * y / total for x, y in number_set.items()}
        decimal_part_with_index = sorted(
            [(strategy, unround_numbers[strategy] % 1) for strategy, value in unround_numbers.items()],
            key=lambda y: y[1], reverse=True)
        remainder = n - sum([int(x) for x in unround_numbers.values()])
        index = 0
        # TODO: Create test for the edge case of all equal proportions
        # TODO: If there are multiple indices that have the same (max) remainder, then add one randomly
        while remainder > 0:
            unround_numbers[decimal_part_with_index[index][0]] += 1
            remainder -= 1
            index = (index + 1) % len(number_set)
        return pd.Series({strategy: int(x) / float(1) for strategy, x in unround_numbers.items()})

    def __str__(self):
        s = []
        for agent in self.agents:
            s += [f"A(ID={agent.ID}, s={agent.strategy}, u={round(agent.utility, 4)}, r={agent.reputation[-1]})"]
        output = "\n".join(s)
        return output


class Experiment:
    """
    Run experiments on variables within the Population class
    """

    @staticmethod
    def generate(name, default, description, variables, values, repeats, export):
        """
        Prepare an experiment on one (or more - not yet implemented) variables. Experiments are run using the time at
        function calling as the seed for the experiment. If experiments are to be reproducible, export the yaml files to
        save the seed state.

        Args:
            name (str): Name of the experiment.
            default (Opgar.Configuration): Default population configuration for all experiments.
            description (str): Description of the experiment.
            variables (list): List of strings containing the variables to be tested.
            values (list): List of values for the variable to be tested.
            repeats (int): The number of times a single test should be repeated.
            export (bool): If True, a yaml file of the experiment configuration will be exported.

        Returns:
            Experiment (dict): Contains the experiment configuration.
        """

        if type(variables) != list:
            raise ValueError(f"Variables must be of type list (not '{type(variables)}').")

        Experiment = {
            "name": name,
            "default": default,
            "description": description,
            "variables": variables,
            "values": values,
            "repeats": repeats,
            "experiments": None,
            "date created": datetime.now(),
        }

        if len(variables) == 1:
            tests = []
            for value in values:
                temp = copy.deepcopy(default)
                setattr(temp, variables[0], value)
                tests.append(temp)
        else:
            tests = []

        # Store datetime as seed for experiment
        Experiment["seed"] = datetime.strftime(Experiment["date created"], "%Y-%m-%d-%H-%M-%S")
        Experiment["experiments"] = {value: experiment for value, experiment in zip(values, tests)}

        if export:
            with open(Experiment["name"] + ".yml", "w") as f:
                yaml.dump(Experiment, f, default_flow_style=False)
                print("Exported yaml experiment")
        return Experiment

    @staticmethod
    def load_experiments(path):
        """
        Load in a yaml file containing an experiment configuration.
        Args:
            path (str): Path to yaml file containing the output of Experiment.generate.

        Returns:
            experiments (dict): Experiment configuration to be passed to Experiment.run_experiments.
        """
        with open(path, "r") as f:
            experiments = yaml.load(f, Loader=yaml.Loader)
        return experiments

    @staticmethod
    def run_experiments(exps, export=False):
        """
        Run a series of experiments given the experiment dictionary.

        Args:
            exps (dict): Dictionary of experiment information (output from Experiment.generate or Experiment.load_experiments).
            export (bool): If true, export the results as a csv file.

        Returns:
            df (pandas.DataFrame): Multi-index Dataframe containing results.
        """

        # set the seed according to the seed in the experiment yaml
        random.seed(exps['seed'])
        results = {}.fromkeys(exps['values'], 0)
        for value, config in exps['experiments'].items():
            P = Population(config)
            results[value] = P.simulate()
        df = pd.concat(results.values(), keys=results.keys(), axis=0, names=["Variable"])

        if export:
            df.to_csv(exps["name"] + ".csv")

        return df
