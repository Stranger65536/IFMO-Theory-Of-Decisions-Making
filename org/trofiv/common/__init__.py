# coding=utf-8
from logging import DEBUG, basicConfig, getLogger

from plotly.graph_objs import Figure, Heatmap, Layout, Surface
from plotly.offline import plot
from preconditions import preconditions
from tqdm import tqdm


class LoggingUtils(object):
    """
    Utility class for logging purposes: progressbar,
    log records and etc.
    """
    basicConfig(level=DEBUG,
                format='%(asctime)s '
                       '%(levelname)s '
                       '%(name)s '
                       '%(message)s ',
                datefmt='%d-%m-%Y %H:%M:%S')

    @staticmethod
    def get_logger(name):
        """
        Returns configured logger with the specified name
        :param name: name of logger
        :return: Logger
        """
        return getLogger(name)

    @staticmethod
    def get_progressbar(label, maxvalue):
        """
        Returns progressbar for the specified label and progress count
        :param label: label for progressbar
        :param maxvalue: max number of updates
        :return: ProgressBar
        """
        progressbar = tqdm(range(maxvalue))
        progressbar.set_description(label)
        return progressbar


class PlotUtils(object):
    """
    Utility class for plotting
    """

    @staticmethod
    @preconditions(lambda x: x.ndim == 1,
                   lambda y: y.ndim == 1,
                   lambda z: z.ndim == 2)
    def plot_surface(x, y, z, title=''):
        """
        Plots specified surface
        :param x: x-axis 1-d arrays
        :param y: y-axis 1-d arrays
        :param z: z-axis 2-d arrays
        :param title: title of plot
        """
        data = [Surface(x=x, y=y, z=z)]
        layout = Layout(title=title, autosize=True)
        fig = Figure(data=data, layout=layout)
        plot(fig, filename=title + '.html')

    @staticmethod
    @preconditions(lambda x: x.ndim == 1,
                   lambda y: y.ndim == 1,
                   lambda z: z.ndim == 2)
    def plot_heatmap(x, y, z, title=''):
        """
        Plots specified heatmap
        :param x: x-axis 1-d arrays
        :param y: y-axis 1-d arrays
        :param z: z-axis 2-d arrays
        :param title: title of plot
        """
        data = [Heatmap(x=x, y=y, z=z)]
        layout = Layout(title=title, autosize=True)
        fig = Figure(data=data, layout=layout)
        plot(fig, filename=title + '.html')

