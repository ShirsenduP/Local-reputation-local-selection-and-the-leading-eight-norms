from setuptools import setup, find_packages

setup(
    name="CodeEvolution",
    version="2020.04",
    packages=find_packages(exclude=['*test']),
    install_requires=['matplotlib', 'networkx',
                      'numpy', 'pandas', 'tqdm', 'scipy']
)
