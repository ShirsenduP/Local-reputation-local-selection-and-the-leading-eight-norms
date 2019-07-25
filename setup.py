from setuptools import setup, find_packages

setup(
	name="CodeEvolution",
	version="0.1.0",
	packages=find_packages(exclude=['*test']),
	install_requires=['matplotlib', 'networkx', 'numpy', 'pandas', 'oct2py', 'tqdm']
)
