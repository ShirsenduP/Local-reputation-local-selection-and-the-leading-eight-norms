import logging
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from collections import OrderedDict


def getDataFromID(ID):
    """When given a jobID, return the data in all the .csv files corresponding to that job. For cluster jobs
    only."""
    dir, _ = os.path.split(os.getcwd())
    dir, _ = os.path.split(dir)  # TODO: while loop to recurse through higher directories til file found
    # print(dir)
    remoteData = os.path.join(dir, 'RemoteData')

    # Search for directory with the .csv files
    path = None
    for root, dirs, files in os.walk(remoteData):
        for name in dirs:
            if ID in name:
                # print(name)
                path = os.path.join(root, name)

    if path is None:
        raise FileNotFoundError(f"Experiment results with id {ID} not found.")

    # Get only the csv files
    files = sorted(os.listdir(path))
    for file in files:
        if '.csv' not in file:
            files.remove(file)
    logging.info(f'files are in {path}')

    # Load panda dataframe results
    dataDict = {}
    for file in files:
        with open(os.path.join(path, file)) as f:
            _, name = os.path.split(f.name)
            name2 = os.path.splitext(name)
            dataDict[int(name2[0])] = pd.read_csv(f)

    # Sort the data so it is plotted in the correct order
    fileNames = sorted(dataDict.keys())
    orderedDataDict = OrderedDict()
    for name in fileNames:
        orderedDataDict[name] = dataDict[name]
    # print(orderedDataDict.keys())
    return orderedDataDict


def getStrategyLabels():
    labelForGraphs = list(range(8))
    for i in range(len(labelForGraphs)):
        labelForGraphs[i] = "$s_{" + str(labelForGraphs[i]) + "}$"
    return labelForGraphs


def plotCooperationProportion(data):
    """Given the job ID of an experiment in the RemoteData directory, plot the average final proportions of
    cooperation. Optionally save plot as .png in dataPath directory."""

    # Get the average proportion of the main strategy in the population
    length = data[0].shape[0]
    means = [round(table['Prop. of Cooperators'].mean(), 5) for ID, table in data.items()]
    # [print(key) for key, value in data.items()]
    standardErrors = [round(table['Prop. of Cooperators'].std() / np.sqrt(length), 5) for ID, table in
                      data.items()]
    fig, ax = plt.subplots()
    strategies = list(range(len(means)))
    ax.errorbar(strategies, means,
                yerr=standardErrors,
                ecolor='grey',
                solid_capstyle='projecting',
                capsize=5,
                elinewidth=2,
                markeredgewidth=2)

    return fig, ax


def plotSingleStrategy(data, strategyID):
    """Given the normal output from getDataFromID, the 'data' is an OrderedDict object with the keys as the several
    values of the parameter being tested, and the values are the standard results table for each corresponding
    parameter."""

    # Get the average proportion of the main strategy in the population
    means = [round(table[f'Prop. Strategy #{strategyID}'].mean(), 5) for _, table in data.items()]
    stds = [round(table[f'Prop. Strategy #{strategyID}'].std(), 5) for _, table in data.items()]

    # print(means)
    # print(stds)

    fig, ax = plt.subplots()
    var = list(range(len(means)))
    ax.errorbar(var, means,
                yerr=stds,
                ecolor='grey',
                solid_capstyle='projecting',
                capsize=5,
                elinewidth=2,
                markeredgewidth=2)

    return fig, ax


def plotAllStrategyCooperations(listOfJobIDs, strategyIDs, skip=[]):
    """Given a list of job IDs and the corresponding strategy IDs in the same order, plot all the proportions of
    cooperation on the same plot."""

    fig, ax = plt.subplots()
    for ID, strategyID in zip(listOfJobIDs, strategyIDs):
        if strategyID in skip:
            continue
        data = getDataFromID(ID)
        length = data[0].shape[0]
        means = [round(table['Prop. of Cooperators'].mean(), 5) for _, table in data.items()]
        stds = [round(table['Prop. of Cooperators'].std() / np.sqrt(length), 5) for _, table in data.items()]
        var = list(range(len(means)))
        up = [mean + std for mean, std in zip(means, stds)]
        down = [mean - std for mean, std in zip(means, stds)]
        plt.plot(var, means, label=f'$s_{strategyID}$')
        plt.fill_between(var, down, up, alpha=0.1, antialiased=True)


def plotAllStrategyProportions(listOfJobIDs, strategyIDs, skip=[]):
    """Given a list of job IDs and the corresponding strategy IDs in the same order, plot all the proportions of
    cooperation on the same plot."""

    fig, ax = plt.subplots()
    for ID, strategyID in zip(listOfJobIDs, strategyIDs):
        if strategyID in skip:
            continue
        data = getDataFromID(ID)
        length = data[0].shape[0]
        means = [round(table[f'Prop. Strategy #{strategyID}'].mean(), 5) for _, table in data.items()]
        stds = [round(table[f'Prop. Strategy #{strategyID}'].std() / np.sqrt(length), 5) for _, table in data.items()]
        var = list(range(len(means)))
        up = [mean + std for mean, std in zip(means, stds)]
        down = [mean - std for mean, std in zip(means, stds)]
        plt.plot(var, means, label=f'$s_{strategyID}$')
        plt.fill_between(var, down, up, alpha=0.1, antialiased=True)


def plotAllStrategiesForVariableCooperation(jobIDs, strategyIDs, skip=[]):
    """Given a list of job IDs, their corresponding strategy IDs, and a list of IDs to be skipped, plot the average
    proportion of the main strategy in the population as a function of a variable to be tested. This will layer the
    line plots (of each strategy) on the same plot."""

    fig, ax = plt.subplots()
    for jobID, strategyID in zip(jobIDs, strategyIDs):
        if strategyID in skip:
            continue
        data = getDataFromID(jobID)
        length = data[0].shape[0]
        means = [round(table['Prop. of Cooperators'].mean(), 5) for _, table in data.items()]
        stds = [round(table['Prop. of Cooperators'].std() / np.sqrt(length), 5) for _, table in data.items()]
        var = list(range(len(means)))
        up = [mean + std for mean, std in zip(means, stds)]
        down = [mean - std for mean, std in zip(means, stds)]
        plt.plot(var, means, label=f'$s_{strategyID}$')
        plt.fill_between(var, down, up, alpha=0.1, antialiased=True)


def plotLeadingEightProportions(jobIDs, models):
    """Plot the final average proportion of all strategies on a single graph"""
    markers = ['s', 'o', 'h']
    fig, ax = plt.subplots()
    for jobID, model, marker in zip(jobIDs, models, markers):
        data = getDataFromID(jobID) # keys are strategies, values are the tables
        length = data[0].shape[0]
        means = [round(table[f'Prop. Strategy #{strategyID}'].mean(), 5) for strategyID, table in data.items()]
        stds = [round(table[f'Prop. Strategy #{strategyID}'].std() / np.sqrt(length), 5) for strategyID,
                                                                                             table in data.items()]
        var = list(range(len(means)))
        plt.errorbar(var, means,
                    yerr=stds,
                    lw=0.2,
                    ms=2,
                    solid_capstyle='projecting',
                    capsize=4,
                    marker='o',
                    elinewidth=2,
                    markeredgewidth=4,
                    label=f'{model}')
#
# def plotAllStrategiesSummary(jobIDs, strategyIDs):
#     """Given the job ID of an experiment in the RemoteData directory, plot the means of the proportions of mutants
#     amongst each strategy along with error bars. Optionally save plot as .png in dataPath directory."""
#
#     # Get the average proportion of the main strategy in the population
#     # length = data[0].shape[0]
#     # means = [round(table[f'Prop. Strategy #{ID}'].mean(), 5) for ID, table in data.items()]
#     # stds = [round(table[f'Prop. Strategy #{ID}'].std() / np.sqrt(length), 5) for ID, table in data.items()]
#     # up = [mean + std for mean, std in zip(means, stds)]
#     # down = [mean - std for mean, std in zip(means, stds)]
#     #
#     fig, ax = plt.subplots()
#
#     for jobID, strategyID in zip(jobIDs, strategyIDs):
#         if strategyID in skip:
#             continue
#         data = getDataFromID(jobID)
#         length = data[0].shape[0]
#         means = [round(table['Prop. of Cooperators'].mean(), 5) for _, table in data.items()]
#         stds = [round(table['Prop. of Cooperators'].std() / np.sqrt(length), 5) for _, table in data.items()]
#         var = list(range(len(means)))
#         up = [mean + std for mean, std in zip(means, stds)]
#         down = [mean - std for mean, std in zip(means, stds)]
#         plt.plot(var, means, label=f'$s_{strategyID}$')
#         plt.fill_between(var, down, up, alpha=0.1, antialiased=True)
#
#     # strategies = list(range(8))
#     # ax.errorbar(strategies, means,
#     #             yerr=stds,
#     #             ecolor='grey',
#     #             solid_capstyle='projecting',
#     #             capsize=5,
#     #             elinewidth=2,
#     #             markeredgewidth=2)
#
#     # plt.rcParams.update({'font.size': 40})
#
#     return fig, ax
#