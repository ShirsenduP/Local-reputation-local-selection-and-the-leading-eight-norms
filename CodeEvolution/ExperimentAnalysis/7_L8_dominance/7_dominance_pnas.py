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

def set_size(w,h, ax=None):
    """ w, h: width, height in inches """
    if not ax: ax=plt.gca()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)

if __name__ == '__main__':

    jobIDs = ['1536568', '1536569', '1536570']
    models = ['LrGe', 'LrLe', 'GrLe']

    # 2 Subplots to show the two y regions of interesting data on a split plot
    f, (ax, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    f.set_size_inches(3.5, 2.5)

    for jobID, model in zip(jobIDs, models):
        data = getDataFromID(jobID)  # keys are strategies, values are the tables
        length = data[0].shape[0]
        means = [round(table[f'Prop. Strategy #{strategyID}'].mean(), 5) for strategyID, table in data.items()]
        stds = [round(table[f'Prop. Strategy #{strategyID}'].std() / np.sqrt(length), 5) for strategyID,
                                                                                             table in data.items()]
        var = list(range(1, len(means)+1))

        # Plot all the data on both axes
        ax.errorbar(var, means,
                    yerr=stds,
                    lw=0,
                    ms=1,
                    solid_capstyle='projecting',
                    capsize=1,
                    marker='x',
                    elinewidth=2,
                    markeredgewidth=4,
                    label=f'{model}')
        ax2.errorbar(var, means,
                     yerr=stds,
                     lw=0,
                     ms=1,
                     solid_capstyle='projecting',
                     capsize=1,
                     marker='x',
                     elinewidth=2,
                     markeredgewidth=4,
                     label=f'{model}')
        ax3.errorbar(var, means,
                     yerr=stds,
                     lw=0,
                     ms=1,
                     solid_capstyle='projecting',
                     capsize=1,
                     marker='x',
                     elinewidth=2,
                     markeredgewidth=4,
                     label=f'{model}')
    # Zoom in on interesting regions
    ax.set_ylim(0.99, 1)
    ax2.set_ylim(0.7, 0.95)
    ax3.set_ylim(-0.09, 0.1)

    # Remote spines between axes
    ax.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax2.axes.get_xaxis().set_visible(False)
    ax.xaxis.tick_top()
    # ax.tick_params(labeltop='off')  # don't put tick labels at the top
    # ax2.tick_params(labeltop='off')  # don't put tick labels at the top
    ax3.xaxis.tick_bottom()

    # Spine cut lines
    d = .01  # how big to make the diagonal lines in axes coordinates
    kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
    ax.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
    ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    kwargs = dict(transform=ax2.transAxes, color='k', clip_on=False)
    ax2.plot((-d, +d), (-d, +d), **kwargs)  # top-left diagonal
    ax2.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax3.transAxes)  # switch to the bottom axes
    ax3.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax3.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    # ax.title.set_text('Average Final Strategy Proportion')
    f.suptitle('TITLE', fontsize=10)
    f.text(0, 0.5, 'Strategy Proportion', va='center', rotation='vertical')
    plt.xlabel('Strategy')
    plt.legend(loc='center_baseline')
    plt.tight_layout()

    plt.savefig('7A_leading4_PNAS', dpi=100)
    # plt.show()
