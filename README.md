# Evolution of Cooperation 

## Description 

This package provides the code to simulate social dilemma games on a large network through indirect repiprocity. It is used to study the evolution of cooperation and to test which of the "Leading Eight" strategies [citation] remain dominant against AllD or AllC and against each other. 

## Installation Instructions

1. Clone the repo with `git clone https://github.com/ShirsenduP/CodeEvolution.git`

2. Move into the new CodeEvolution directory using `cd CodeEvolution`

3. Create a virtual environment running python 3.6 (here we call it "env" but you can call it anything) with `python -m venv env` and start the virtual environment with `source env/bin/activate`. [Here](https://itnext.io/virtualenv-with-virtualenvwrapper-on-ubuntu-18-04-goran-aviani-d7b712d906d5) is a useful guide to set up virtual environments if needed.

4. Install package and all its dependencies with `pip install .` or `pip install -e .` if you would like to develop the package further. 

Uninstall with `pip uninstall CodeEvolution`.


## Tutorial

Running a single simulation is fairly straightforward. Examples are also found in `Examples/`.

1. Import the package

    ```python
    import CodeEvolution as ce
    ```

2. Create a configuration the fastest way

    ```python
    config = ce.Config(
        testcase="minimal", # Options: ["minimal", "grle"]
    )  
    ```
    
    or with a custom structure and evolution/reputation mechanism but default parameters

    ```python
    config = ce.Config(
        structure="erdos renyi", # Options: ["erdos renyi", "reg lattice", "power law", "small world"] (see models.py)
        reputation="global", # Options: ["global", "local"] (see reputation.py)
        evolution="global", # Options: ["global", "local"] (see evolution.py)
    )  
    ```

    or by specifying everything

    ```python
    config = ce.Config(
        structure="erdos renyi", # Options: ["erdos renyi", "reg lattice", "power law", "small world"] (see models.py)
        reputation="global", # Options: ["global", "local"] (see reputation.py)
        evolution="global", # Options: ["global", "local"] (see evolution.py)
        size=300,
        initialState=ce.State(mainID=0, proportion=1, mutantID=8),  # (see strategy.py)
        socialDilemma=ce.config.Dilemma(type="PD", benefit=2, cost=1), # Only the "PD" type is available
        omegas=0.99,
        maxPeriods=2000,
        alpha=0.1, 
        delta=1,
        mutationProbability=0.1,
        sparseDensity=True,
        density=None,
        degree=None,
        attachment=None,
        smallWorld=None
    )  
    ```


3. Build a model

    ```python
    model = ce.ceModel.build(config)
    ```

4. Run the simulation

    ```python
    # If fullSeries is True, then pandas.DataFrame is returned with complete dataset, 
    # otherwise only results (as pandas.Series) at convergence is returned.
    results = model.runSimulation(fullSeries=False) 
    ```

## Results
Here is an example set of results (returned as a pandas Series) that would be returned if `fullSeries=False` in the `runSimulation` method. If `fullSeries=True`, then most of the variables described below will exist in a pandas DataFrame instead as a time series. 

    ```python
    Main Prop.                 0.993333     # Proportion of the main strategy
    Mutant Prop.               0.006667     # Proportion of AllD (Id. 8) or AllC (Id. 9)
    Prop. of Cooperators       1.000000     # Proportion of C played in the population
    Prop. of Defectors         0.000000     # Proportion of D played in the population
    Avg. Main Util.            1.000000     # Average utility of the main strategy
    Avg. Mutant Util.          0.000000     # Average utility of the mutant strategy
    Main Vs Main               1.000000     # Proportion of interactions that occurred between two agents of the main strategy
    Mutant Vs Main             0.000000     # Proportion of interactions that occurred between two agents of a different strategy
    Mutant Vs Mutant           0.000000     # Proportion of interactions that occurred between two agents of the mutant strategy
    Main & Good                0.986667     # Proportion of agents that are of the main strategy and have a good reputation
    Main & Bad                 0.006667     # Proportion of agents that are of the main strategy and have a bad reputation
    Mutant & Good              0.000000     # Proportion of agents that are of the mutant strategy and have a good reputation
    Mutant & Bad               0.006667     # Proportion of agents that are of the mutant strategy and have a bad reputation
    Mutants Added            180.000000     # Total number of mutant agents added in the population
    Main ID                    0.000000     # ID of the main strategy (0-7 are the leading eight)
    Main Initial Prop.         1.000000     # Initial proportion of the main strategy
    Mutant ID                  8.000000     # ID of the mutant strategy (8 is AllD and 9 is AllC)
    Mutant Initial Prop.       0.000000     # Initial proportion of the mutant strategy
    Tmax                    1999.000000     # The maximum timestep reached in the simulation (by reaching max periods or by convergence)
    Name: 1999, dtype: float64
    ```

## Contributors
Shirsendu Podder, UCL, _ucabpod@ucl.ac.uk_ \
Simone Righi, UCL, _s.righi@ucl.ac.uk_ 
