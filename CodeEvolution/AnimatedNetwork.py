import random

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.animation import FuncAnimation

from CodeEvolution.config import Config, State
from CodeEvolution.models import LrGeERNetwork

matplotlib.use("TkAgg")
np.random.seed(1)
random.seed(1)

frames = 100
times = [f"t={i}" for i in range(frames)]


def node_colour_from_strategies():
    """Given a list of strategies, assign blue to main ID agents, red to mutant ID agents"""
    return np.array([agent.Strategy.ID / 9 for agent in N.agentList])


def update(n):
    N.runSingleTimestep()
    N.evolutionaryUpdate()
    N.mutate(8)
    nc = node_colour_from_strategies()
    print(f"{n}", N._getCensus(True))
    nodes.set_array(nc)
    return nodes,


def update_text(num):
    time_text.set_text(times[num])
    return time_text,


fig = plt.figure(figsize=(8, 8))
time_text = plt.text(0, 0, '', fontsize=15)

C = Config(size=50,
           initialState=State(0, 0.5, 8),
           sparseDensity=True,
           alpha=1,
           mutationProbability=0.5)

N = LrGeERNetwork(C)

G = nx.Graph()

G.add_nodes_from(N.agentList)
for agent in N.agentList:
    for nbr in agent.neighbours:
        G.add_edge(agent, nbr)

pos = nx.random_layout(G)
nodes = nx.draw_networkx_nodes(G, pos=pos, node_color=node_colour_from_strategies())
edges = nx.draw_networkx_edges(G, pos)

#

anim = FuncAnimation(fig, func=update, interval=250, blit=False, frames=frames)
anim2 = FuncAnimation(fig, func=update_text, interval=250, blit=False)
plt.show()
