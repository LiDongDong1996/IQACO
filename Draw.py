import matplotlib.pyplot as plt
import matplotlib.patches as pat
import numpy as np

class GridPlot:
    def __init__(self, map_data, x_label='', y_label='', x_major=1, y_major=1, obs_color="k", edge_color='k') -> None:
        self.map_size = np.array([*map_data.shape])  # Get map dimensions
        default_size = np.array([7, 7])  # Default figure size
        self.fig = plt.figure(figsize=default_size * (self.map_size[::-1] / max(self.map_size[::-1])))
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax1.set_xbound(0, len(map_data))
        self.ax1.set_ybound(0, len(map_data))
        rect_patches = []
        for ki, row in enumerate(map_data):
            for kj, cell in enumerate(row):
                if cell == 1:
                    rect_patches.append(pat.Rectangle((kj, ki), 1, 1, color=obs_color))
                else:
                    rect_patches.append(pat.Rectangle((kj, ki), 1, 1, fill=False, edgecolor=edge_color, linewidth=1))
        for patch in rect_patches:
            self.ax1.add_patch(patch)
        self.ax1.set_xlabel(x_label)
        self.ax1.set_ylabel(y_label)
        # Set tick labels
        self.ax1.set_xticks(np.array([1] + list(np.arange(x_major, map_data.shape[1] + 1, x_major))) - 0.5)
        self.ax1.set_yticks(np.array([1] + list(np.arange(y_major, map_data.shape[0] + 1, y_major))) - 0.5)
        # Set tick labels starting from 1 with specified intervals
        self.ax1.set_xticklabels([1] + list(np.arange(x_major, map_data.shape[1] + 1, x_major)))
        self.ax1.set_yticklabels([1] + list(np.arange(y_major, map_data.shape[0] + 1, y_major)))
        self.show_legend = False
        self.handles = []  # Store plot handles for legend

    def draw_path(self, path_data, style_dict={}):
        """
        Draw a path on the grid, accepting all parameters supported by plt.plot via dictionary unpacking.

        Parameters
        ----------
        path_data : list or np.ndarray
            Path coordinates in [y, x] format.
        style_dict : dict
            Parameters supported by plt.plot, such as color, linestyle, marker, label, linewidth, etc.
        """
        path_data = np.array(path_data)

        if 'label' in style_dict:
            self.show_legend = True

        lines, = self.ax1.plot(
            path_data[:, 1] + 0.5,
            path_data[:, 0] + 0.5,
            **style_dict
        )
        self.handles.append(lines)  # Store the line handle for legend

    def show(self):
        if self.show_legend:
            self.ax1.legend()
        plt.show()

    def save(self, filename='figure.jpg'):
        if self.show_legend:
            self.ax1.legend()
        plt.savefig(filename)

class IterationGraph:
    def __init__(self, data_list, style_dict_list=[], point_interval=1) -> None:
        '''
        Function
        --------
        Plot iteration data as a graph.

        Parameters
        ----------
        data_list : list
            List of 1D arrays containing iteration data.
        style_dict_list : list
            List of dictionaries with plot style parameters (e.g., color, linestyle, marker, label, linewidth).
        point_interval : int
            Interval for plotting points, default is 1.

        Returns
        -------
        None
        '''
        self.fig, self.ax = plt.subplots()
        self.data_list = data_list  # Store data for future use

        for i in range(len(data_list)):
            x_values = range(len(data_list[i]))
            if len(style_dict_list) > i:
                self.ax.plot(
                    x_values[::point_interval],
                    data_list[i][::point_interval],
                    **style_dict_list[i])
            else:
                self.ax.plot(
                    x_values[::point_interval],
                    data_list[i][::point_interval]
                )

    def show(self):
        plt.show()

    def save(self, filename='figure.jpg'):
        self.fig.savefig(filename)


