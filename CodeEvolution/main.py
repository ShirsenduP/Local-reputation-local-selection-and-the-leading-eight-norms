import matplotlib.pyplot as plt
import networkx as nx
import random

from network import Network
from agent import Agent

def main():

	size = 10
	density = 0.5
	omega = 0

	N = Network(_size=size, _density=density, _omega=omega)
	N.show()
	N.summary()

	

	return 0

if __name__ == "__main__":
	main()



# TODO:
# 1. Setup as package so it can easily be installed on any linux system with help docs. 
# 2. Create builder class to setup parameters of model, then change Network class to just accept a builder object to seperate the config methods to the simulation methods
# 3. When adding neighbours, don't add if already neighbours! repeated agents in agent.neighbours list!




