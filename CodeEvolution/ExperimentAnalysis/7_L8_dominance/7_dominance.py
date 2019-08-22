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

if __name__ == '__main__':

    jobIDs = ['1536567', '1536568', '1536569', '1536570']
    models = ['GrGe', 'LrGe', 'LrLe', 'GrLe']

    for jobID, model in zip(jobIDs, models):
        data = getDataFromID(jobID)

        fig, ax = plotAllStrategiesSummary(data)
        plt.title(f'{model} - Leading Eight vs All-D')
        plt.xlabel("Strategy ID")
        plt.ylabel(f"Average Final Proportion")
        plt.savefig(jobID + "_" + model)
