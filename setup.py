from setuptools import setup

setup(
    name="CodeEvolution",
    version="2020.06.01",
    packages=["leading"],
    package_dir={
        "leading": "CodeEvolution/Leading",
    },
    install_requires=['matplotlib', 'networkx',
                      'numpy', 'pandas', 'tqdm', 'scipy', 'pytest']
)
