"""
Experiment 7.x

Testing the dominance of the leading 8 on these setups of networks

    ER:
        7A_a    1536567     GrGe
        7A_b    1536568     LrGe
        7A_c    1536569     LrLe
        7A_d    1536570     GrLe

Source: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html#sphx-glr-galle
        ry-lines-bars-and-markers-horizontal-barchart-distribution-py

"""

import numpy as np
from matplotlib import pyplot as plt

if __name__=="__main__":
    category_names = ['Group I', 'Group II', 'Group III']
    leading_strategies = {
        'GrGe': [2, 4, 2],
        'LrGe': [2, 0, 2],
        'GrLe': [2, 4, 2],
        'LrLe': [2, 4, 2],
        }


    def survey(results, category_names):
        """
        Parameters
        ----------
        results : dict
            A mapping from question labels to a list of answers per category.
            It is assumed all lists contain the same number of entries and that
            it matches the length of *category_names*.
        category_names : list of str
            The category labels.
        """
        labels = list(results.keys())
        data = np.array(list(results.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.get_cmap('RdYlGn')(
            np.linspace(0.15, 0.85, data.shape[1]))

        fig, ax = plt.subplots(figsize=(9.2, 5))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            ax.barh(labels, widths, left=starts, height=0.5,
                    label=colname, color=color)
            xcenters = starts + widths / 2

            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            for y, (x, c) in enumerate(zip(xcenters, widths)):
                ax.text(x, y, str(int(c)), ha='center', va='center',
                        color=text_color)
        ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                  loc='lower left', fontsize='small')

        return fig, ax

survey(leading_strategies, category_names)
plt.show()