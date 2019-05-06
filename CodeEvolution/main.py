import matplotlib.pyplot as plt
import networkx as nx

from network import Network
from agent import Agent


def main():

	size = 15
	density = 0.7

	N = Network(_size=size, _density=density)
	N.summary()
	

if __name__ == "__main__":
	main()
