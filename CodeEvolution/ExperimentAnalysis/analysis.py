import os
import pandas as pd
import matplotlib.pyplot as plt


def getDataFromID(ID):
    """When given a jobID, return the data in all the .csv files corresponding to that job. For cluster jobs
    only."""
    dir, _ = os.path.split(os.getcwd()) # TODO this when running outside of the ExperimentAnalysis dir breaks!
    print(dir)
    remoteData = os.path.join(dir, 'RemoteData')

    # Search for directory with the .csv files
    path = None
    for root, dirs, files in os.walk(remoteData):
        for name in dirs:
            if ID in name:
                print(name)
                path = os.path.join(root, name)

    if path is None:
        raise FileNotFoundError(f"Experiment results with id {ID} not found.")

    # Get only the csv files
    files = sorted(os.listdir(path))
    for file in files:
        if '.csv' not in file:
            files.remove(file)

    # Load panda dataframe results
    dataDict = {}
    for file in files:
        with open(os.path.join(path, file)) as f:
            _, name = os.path.split(f.name)
            name2 = os.path.splitext(name)
            dataDict[int(name2[0])] = pd.read_csv(f)

    return dataDict


def getStrategyLabels():
    labelForGraphs = list(range(8))
    for i in range(len(labelForGraphs)):
        labelForGraphs[i] = "$s_{" + str(labelForGraphs[i]) + "}$"
    return labelForGraphs


def plotAllStrategiesSummary(data, filename=None):
    """Given the job ID of an experiment in the RemoteData directory, plot the means of the proportions of mutants
    amongst each strategy along with error bars. Optionally save plot as .png in dataPath directory."""

    # Get the average proportion of the main strategy in the population
    means = [round(table[f'Prop. Strategy #{ID}'].mean(), 5) for ID, table in data.items()]
    stds = [round(table[f'Prop. Strategy #{ID}'].std(), 5) for ID, table in data.items()]

    fig, ax = plt.subplots()
    strategies = list(range(8))
    ax.errorbar(strategies, means,
                yerr=stds,
                ecolor='grey',
                solid_capstyle='projecting',
                capsize=5,
                elinewidth=2,
                markeredgewidth=2)

    plt.rcParams.update({'font.size': 40})

    return fig, ax


def plotCooperationProportion(data, filename=None):
    """Given the job ID of an experiment in the RemoteData directory, plot the average final proportions of
    cooperation. Optionally save plot as .png in dataPath directory."""

    # Get the average proportion of the main strategy in the population
    means = [round(table['Prop. of Cooperators'].mean(), 5) for ID, table in data.items()]
    stds = [round(table['Prop. of Cooperators'].std(), 5) for ID, table in data.items()]
    print(means)
    print()
    print(stds)
    fig, ax = plt.subplots()
    strategies = list(range(9))
    ax.errorbar(strategies, means,
                yerr=stds,
                ecolor='grey',
                solid_capstyle='projecting',
                capsize=5,
                elinewidth=2,
                markeredgewidth=2)

    # plt.rcParams.update({'font.size': 20})

    return fig, ax