from itertools import product

from CodeEvolution.Leading.strategy import Strategy


class AllStrategies(Strategy):
    allStates = ['11', '10', '01', '00']
    allOutcomes = list(product("CD", repeat=4))


class AllNorms:
    allStates = ['11C', '11D', '10C', '10D', '01C', '01D', '00C', '00D']
    allOutcomes = list(product([1, 0], repeat=8))


class Pair:
    # index = list(product(AllStrategies.allOutcomes, AllNorms.allOutcomes))
    index_map = {i: {"behavioural strategy": j[0], "social norm": j[1]} for i, j in
                 enumerate(product(AllStrategies.allOutcomes, AllNorms.allOutcomes))}


print(Pair.index_map[4095])
