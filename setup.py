from setuptools import setup, find_packages

setup(
	name="EvolutionOfCooperation",
	version="0.0.1",
	packages=find_packages(exclude=['*test']),
	install_requires=['matplotlib', 'networkx']
)