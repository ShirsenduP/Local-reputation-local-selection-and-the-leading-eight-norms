import numpy as np
from matplotlib import pyplot as plt
from CodeEvolution.Evaluator import Evaluator
from CodeEvolution.GrGe import GrGe_Network
from CodeEvolution.LrGe import LrGe_Network
from CodeEvolution.LrLe import LrLe_Network
from CodeEvolution.config import Config
from CodeEvolution.Experiment import Experiment
from CodeEvolution.Experiment import Population


if __name__ == '__main__':
    """Test 3 - Sparse networks, all 8 strategies vs All-D/All-C with 20/80 mutant/population split. """

    rerunSimulations = True

    if rerunSimulations:
        pops = Experiment.generatePopulationList(proportion=0.8)
        reps = 1
        size = 500
        sparseNetworkDensity = 2*np.log(size)/size

        """All-D versus all the populations, initially weighted at 20/80."""

        default = Config(size=size, densities=1, mutant=Population(ID=8, Proportion=0.2))
        E = Experiment(name='GrGe_All-D_Sparse_20:80_', networkType=GrGe_Network, defaultConfig=default,
                       variable='population', values=pops,
                       repeats=reps)
        E.run(display=True)
        #
        # default2 = Config(size=size, densities=sparseNetworkDensity, mutant=Population(ID=8, Proportion=0.2))
        # E2 = Experiment(name='LrGe_All-D_Sparse_20:80_', networkType=LrGe_Network, defaultConfig=default2,
        #                 variable='population', values=pops,
        #                 repeats=reps)
        # E2.run(export=True)
        #
        # default3 = Config(size=size, densities=sparseNetworkDensity, mutant=Population(ID=8, Proportion=0.2))
        # E3 = Experiment(name='LrLe_All-D_Sparse_20:80_', networkType=LrLe_Network, defaultConfig=default3,
        #                 variable='population', values=pops,
        #                 repeats=reps)
        # E3.run(export=True)
        #
        # """All-C versus all the populations, initially weighted at 10/90."""
        # #
        # default4 = Config(size=size, densities=sparseNetworkDensity, mutant=Population(ID=9, Proportion=0.2))
        # E4 = Experiment(name='GrGe_All-C_Sparse_20:80_', networkType=GrGe_Network, defaultConfig=default4,
        #                 variable='population', values=pops,
        #                 repeats=reps)
        # E4.run(export=True)
        #
        # default5 = Config(size=size, densities=sparseNetworkDensity, mutant=Population(ID=9, Proportion=0.2))
        # E5 = Experiment(name='LrGe_All-C_Sparse_20:80_', networkType=LrGe_Network, defaultConfig=default5,
        #                 variable='population', values=pops,
        #                 repeats=reps)
        # E5.run(export=True)
        #
        # default6 = Config(size=size, densities=sparseNetworkDensity, mutant=Population(ID=9, Proportion=0.2))
        # E6 = Experiment(name='LrLe_All-C_Sparse_20:80_', networkType=LrLe_Network, defaultConfig=default6,
        #                 variable='population', values=pops,
        #                 repeats=reps)
        # E6.run(export=True)

    # # Plots
    #
    # GrGe_AllD = Evaluator.open_results("type_population_2019-07-07 00:48")
    # LrGe_AllD = Evaluator.open_results("type_population_2019-07-07 01:32")
    # LrLe_AllD = Evaluator.open_results("type_population_2019-07-07 02:15")
    # GrGe_AllC = Evaluator.open_results("type_population_2019-07-07 03:00")
    # LrGe_AllC = Evaluator.open_results("type_population_2019-07-07 03:45")
    # LrLe_AllC = Evaluator.open_results("type_population_2019-07-07 04:30")
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
