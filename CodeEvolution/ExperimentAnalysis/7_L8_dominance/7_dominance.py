"""
Experiment 7

Testing the dominance of the leading 8 on these setups of networks

    ER:
        7A_a    1536567     GrGe
        7A_b    1536568     LrGe
        7A_c    1536569     LrLe
        7A_d    1536570     GrLe

"""

from CodeEvolution.ExperimentAnalysis.analysis import *
from CodeEvolution.Evaluator import Evaluator

if __name__ == '__main__':
    #####################################################################
    jobID = '1536567'
    data = getDataFromID(jobID)

    fig, ax = plotAllStrategiesSummary(data)
    plt.title('GrGe - Leading Eight vs All-D')
    plt.xlabel("Strategy ID")
    plt.ylabel(f"Average Final Proportion")
    plt.show()
    #####################################################################
    jobID = '1536568'
    data = getDataFromID(jobID)

    fig, ax = plotAllStrategiesSummary(data)
    plt.title('LrGe - Leading Eight vs All-D')
    plt.xlabel("Strategy ID")
    plt.ylabel(f"Average Final Proportion")
    plt.show()
    #####################################################################
    jobID = '1536569'
    data = getDataFromID(jobID)

    fig, ax = plotAllStrategiesSummary(data)
    plt.title('LrLe - Leading Eight vs All-D')
    plt.xlabel("Strategy ID")
    plt.ylabel(f"Average Final Proportion")
    plt.show()
    #####################################################################
    jobID = '1536570'
    data = getDataFromID(jobID)

    fig, ax = plotAllStrategiesSummary(data)
    plt.title('GrLe - Leading Eight vs All-D')
    plt.xlabel("Strategy ID")
    plt.ylabel(f"Average Final Proportion")
    plt.show()