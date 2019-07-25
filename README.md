# Evolution of Cooperation 

## Description 

This package provides the code to simulate social dilemna games on a large network through indirect repiprocity. It is used to study the evolution of cooperation and to test which of the "Leading Eight" strategies [citation] remain dominant against AllD or AllC and against each other. 

## Setup Instructions (local)

1. Clone the repo with `git clone https://github.com/ShirsenduP/CodeEvolution.git`

2. Move into the CodeEvolution directory using `cd CodeEvolution`

3. Create a virtual environment running python 3.6 (here we call it "env" but you can call it anything) with `virtualenv --python=python3.6 env` and start the virtual environment with `source env/bin/activate`

4. Install package and all its dependencies with `python setup.py install`. 

Uninstall with `pip uninstall CodeEvolution`.

## Setup Instructions (UCL clusters)

1. Log into UCL Myriad and use `cd Scratch` to move into the Scratch directory.

2. Load recommended python modules with `module load python3/recommended`.

3. Clone the repo with `git clone https://github.com/ShirsenduP/CodeEvolution.git`.

4. Move into the CodeEvolution directory using `cd CodeEvolution`.

5. Create a virtual environment running python 3.6 (here we call it "env" but you can call it anything) with `virtualenv --python=python3.6 env` and initiate the environment with `source env/bin/activate`.

6. Install package and all its dependencies with `python setup.py install`. If this fails, run `python setup.py install --user` (but shouldn't have to as long as you are within the virtual environment).

Uninstall with `pip uninstall CodeEvolution`.


## Contributors
Shirsendu Podder, UCL, _ucabpod@ucl.ac.uk_ \\
Simone Righi, UCL, _s.righi@ucl.ac.uk_ 
