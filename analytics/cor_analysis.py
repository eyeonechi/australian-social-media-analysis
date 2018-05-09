"""
CCC Team 42, Melbourne

Thuy Ngoc Ha - 963370
Lan Zhou - 824371
Zijian Wang - 950618			
Ivan Chee - 736901
Duer Wang - 824325

"""
"""
A simple plotting script
"""

import numpy as np
import matplotlib.pyplot as plt

input_file = 'data/output_negative.csv'
output_file = 'data/neg_t.png'
x_label = 'sentiment score'
y_label = 'homeless trend'


def scatter_plot_with_correlation_line(x, y, graph_filepath):
    # Scatter plot
    plt.scatter(x, y)

    # Add correlation line
    axes = plt.gca()
    m, b = np.polyfit(x, y, 1)
    X_plot = np.linspace(axes.get_xlim()[0],axes.get_xlim()[1],100)
    plt.plot(X_plot, m*X_plot + b, 'r-')

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # Save figure
    plt.savefig(graph_filepath, dpi=300, format='png', bbox_inches='tight')
    

if __name__ == "__main__":

    data = np.loadtxt(input_file, delimiter=',', skiprows=1)

    polarity = data[:, 0]
    homeless = data[:, 2]

    scatter_plot_with_correlation_line(polarity, homeless, output_file)