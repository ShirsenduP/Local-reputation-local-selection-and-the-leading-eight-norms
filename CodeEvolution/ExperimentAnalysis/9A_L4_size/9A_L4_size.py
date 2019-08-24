from CodeEvolution.ExperimentAnalysis.analysis import *

"""
Experiment 9A-----------------------------------------------------------------------

Effect of simulation on variance of convergence point, Erdos Renyi network, size 300, test maxT from 500-5000 at
intervals of 250 to see if maxT of 5000 is necessary for every simulation.

    9A_0    1582527 ....
    9A_1    1576515 done
    9A_6    1574515 done
    9A_7    1574516 done

"""

if __name__ == '__main__':

    jobIDs = ['1576515', '1574515', '1574516']
    strategyIDs = [1, 6, 7]

    for strategy, jobID in zip(strategyIDs, jobIDs):
        data = getDataFromID(jobID)
        fig, ax = plotCooperationProportion(data)
        plt.title(f'LrGeER $s_{strategy}$ vs Max Length of Simulation')
        plt.xlabel("$T_{max}$")
        plt.ylabel(f"Average Final Proportion of Cooperation")
        xpos, xticks = range(0, 20, 2), list(range(500, 5001, 500))
        plt.xticks(xpos, xticks, rotation=45)
        plt.savefig(jobID + "_cooperation")
        # plt.show()
