import random
import networkx as nx
import matplotlib.pyplot as plt
import agent

#Generate randomised adjacency matrices

for i in range(10):
    G = nx.erdos_renyi_graph(random.randint(1,50), random.uniform(0,1), seed=None, directed=False)

    for line in nx.generate_adjlist(G):
        print(line)

    nx.write_edgelist(G, path='tests/testfile{}'.format(i), delimiter=':')

