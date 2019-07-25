# Evolution of Cooperation 

## Description 

This package provides the code to simulate social dilemna games on a large network through indirect repiprocity. It is used to study the evolution of cooperation and to test which of the "Leading Eight" strategies [citation] remain dominant against AllD or AllC and against each other. 

## Setup Instructions

These are the setup instructions for Linux:

1. Create new folder to save source code, using terminal, navigate to your chosen directory and run `mkdir EvolutionOfCooperation && cd EvolutionOfCooperation`
2. `git clone https://github.com/ShirsenduP/CodeEvolution.git` to a (this will not currently work as it is a private repository)
3. `pip install .` to install package and all dependencies

## New Setup Instructions

1. Clone the repo
`git clone https://github.com/ShirsenduP/CodeEvolution.git`

2. Move into the CodeEvolution directory
`cd CodeEvolution`

3. Create a virtual environment running python 3.6 (here we call it "env" but you can call it anything)
`virtualenv --python=python3.6 env`
and start the virtual environment
`source env/bin/activate`

4. Install package and all its dependencies
`python setup.py install`


## Contributors
Shirsendu Podder, UCL, _ucabpod@ucl.ac.uk_
Simone Righi, UCL, _s.righi@ucl.ac.uk_ 
