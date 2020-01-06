import numpy as np
from matplotlib import pyplot as plt
from CodeEvolution.Evaluator import Evaluator
from CodeEvolution.models import GrGeERNetwork, LrGeERNetwork, LrLeERNetwork
from CodeEvolution.config import Config
from CodeEvolution.Experiment import Experiment
from CodeEvolution.Experiment import Population


if __name__ == '__main__':
    """Test 2 - Sparse networks, all 8 strategies vs All-D/All-C
    Investigating the dominance of the leading 8 in all 3 setups again, now with the density of the network at the 
    minimum likely lambda for a connected network. If we have G(n,p) E-R random network, p = 2*ln(n)/n, with n=500, 
    we take p = 0.024858432393688765. """

    rerunSimulations = True

    if rerunSimulations:
        pops = Experiment.generatePopulationList()
        reps = 25
        size = 500
        sparseNetworkDensity = 2*np.log(size)/size

        """All-D versus all the populations, initially weighted at 10/90."""

        default = Config(densities=1, mutant=Population(ID=8, Proportion=0.1))
        E = Experiment(name='GrGe_All-D_Sparse', networkType=GrGeERNetwork, defaultConfig=default,
                       variable='population', values=pops,
                       repeats=reps)
        E.run(export=True)

        default2 = Config(size=500, densities=sparseNetworkDensity, mutant=Population(ID=8, Proportion=0.1))
        E2 = Experiment(name='LrGe_All-D_Sparse', networkType=LrGeERNetwork, defaultConfig=default2,
                        variable='population', values=pops,
                        repeats=reps)
        E2.run(export=True)

        default3 = Config(size=500, densities=sparseNetworkDensity, mutant=Population(ID=8, Proportion=0.1))
        E3 = Experiment(name='LrLe_All-D_Sparse', networkType=LrLeERNetwork, defaultConfig=default3,
                        variable='population', values=pops,
                        repeats=reps)
        E3.run(export=True)

        """All-C versus all the populations, initially weighted at 10/90."""

        default4 = Config(size=500, densities=sparseNetworkDensity, mutant=Population(ID=9, Proportion=0.1))
        E4 = Experiment(name='GrGe_All-C_Sparse', networkType=GrGeERNetwork, defaultConfig=default4,
                        variable='population', values=pops,
                        repeats=reps)
        E4.run(export=True)

        default5 = Config(size=500, densities=sparseNetworkDensity, mutant=Population(ID=9, Proportion=0.1))
        E5 = Experiment(name='LrGe_All-C_Sparse', networkType=LrGeERNetwork, defaultConfig=default5,
                        variable='population', values=pops,
                        repeats=reps)
        E5.run(export=True)

        default6 = Config(size=500, densities=sparseNetworkDensity, mutant=Population(ID=9, Proportion=0.1))
        E6 = Experiment(name='LrLe_All-C_Sparse', networkType=LrLeERNetwork, defaultConfig=default6,
                        variable='population', values=pops,
                        repeats=reps)
        E6.run(export=True)

    # # Plots
    #
    # GrGe_AllD = Evaluator.open_results("")
    # LrGe_AllD = Evaluator.open_results("")
    # LrLe_AllD = Evaluator.open_results("")
    # GrGe_AllC = Evaluator.open_results("")
    # LrGe_AllC = Evaluator.open_results("")
    # LrLe_AllC = Evaluator.open_results("")
    #
    # GrGe_AllD_Stable_Proportion = Evaluator.getProportionOfStable(GrGe_AllD)
    # GrGe_AllC_Stable_Proportion = Evaluator.getProportionOfStable(GrGe_AllC)
    # LrGe_AllD_Stable_Proportion = Evaluator.getProportionOfStable(LrGe_AllD)
    # LrGe_AllC_Stable_Proportion = Evaluator.getProportionOfStable(LrGe_AllC)
    # LrLe_AllD_Stable_Proportion = Evaluator.getProportionOfStable(LrLe_AllD)
    # LrLe_AllC_Stable_Proportion = Evaluator.getProportionOfStable(LrLe_AllC)
    #
    # labels = Evaluator.getStrategyLabels()
    # x = np.arange(len(labels))
    # width = 0.13
    #
    # fig, ax = plt.subplots(figsize=(10, 3))
    #
    # rects1A = ax.bar(x - 5 * width / 2, GrGe_AllD_Stable_Proportion, width, label='GrGe_All-D')
    # rects1B = ax.bar(x - 3 * width / 2, GrGe_AllC_Stable_Proportion, width, label='GrGe_All-C')
    #
    # rects2A = ax.bar(x - 1 * width / 2, LrGe_AllD_Stable_Proportion, width, label='LrGe_All-D')
    # rects2B = ax.bar(x + 1 * width / 2, LrGe_AllC_Stable_Proportion, width, label='LrGe_All-C')
    #
    # rects3A = ax.bar(x + 3 * width / 2, LrLe_AllD_Stable_Proportion, width, label='LrLe_All-D')
    # rects3B = ax.bar(x + 5 * width / 2, LrLe_AllC_Stable_Proportion, width, label='LrLe_All-C')
    #
    # ax.set_title('Proportions of the leading eight that remain stable against All-C/D')
    # ax.set_xticks(x)
    # ax.set_ylabel('Proportion of Simulations \nwith stable strategy')
    #
    # ax.set_xticklabels(labels)
    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0 - box.height * 0.15, box.width, box.height * 1.2])
    #
    # fig.legend(loc='lower center', bbox_to_anchor=(0.5, 0.03), fancybox=True, shadow=True, ncol=6)
    # plt.show()
    # # fig.savefig('Leading8_density_too_high')
