from setuptools import setup, find_packages

setup(
    name="CodeEvolution",
    version="2020.06.01",
    packages=["leading", "opgar"],
    package_dir={
        "leading": "CodeEvolution/Leading",
        "opgar": "CodeEvolution/Opgar",
    },
    install_requires=['matplotlib', 'networkx',
                      'numpy', 'pandas', 'tqdm', 'scipy', 'pytest', 'pyyaml']
)
