from setuptools import setup

setup(
    name="CodeEvolution",
    version="2020.06.01",
    packages=["CodeEvolution"],
    package_dir={
        "CodeEvolution": "CodeEvolution",
    },
    install_requires=[
        "matplotlib",
        "networkx",
        "numpy",
        "pandas",
        "tqdm",
        "scipy",
        "pytest",
    ],
)
