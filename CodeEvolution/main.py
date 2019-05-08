import matplotlib.pyplot as plt
import networkx as nx

from network import Network
from agent import Agent


def main():

	size = 15
	density = 0.32

	N = Network(_size=size, _density=density)
	# N.summary()
	# N.show()
	print(N.chooseTwoAgents())
	return 0

if __name__ == "__main__":
	main()



# TODO:
# 1. Setup as package so it can easily be installed on any linux system with help docs. 
