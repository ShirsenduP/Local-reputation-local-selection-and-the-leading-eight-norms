from setuptools import setup, find_packages

setup(
    name="CodeEvolution",
    version="2020.04.01",
    packages=find_packages("CodeEvolution"),
    install_requires=['matplotlib', 'networkx',
                      'numpy', 'pandas', 'tqdm', 'scipy']
)
