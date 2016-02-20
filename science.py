"""
Matplotlib. Wrapper. Smart. Tufte. Pythonic.
"""

from types import GeneratorType
import matplotlib
from matplotlib import pyplot

class Plot:
    bars = False
    grid = False
    fill = False
    bars_width = 1

    @staticmethod
    def count(samples, bins=None, **options):
        if bins is None:
            bins = 1
        if isinstance(bins, int):
            bins = range(0, max(samples), bins)

        data = {k: 0 for k in bins}
        for sample in samples:
            if sample >= bins[-1]:
                bin = bins[-1]
            else:
                bin = next(bin_start
                    for bin_start, bin_end in zip(bins, bins[1:])
                    if bin_start <= sample < bin_end)
            data[bin] += 1

        options.setdefault('bars', True)
        plot = Plot(data, **options)
        plot.bars_width = [bin_end - bin_start for bin_start, bin_end in zip(bins, bins[1:])] + [bins[-1] - bins[-2]]
        return plot

    def __init__(self, data, title='', xlabel='', ylabel='', **options):
        if isinstance(data, (list, tuple, GeneratorType, range)):
            data = dict(enumerate(data))

        self.data = data
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        
        for option, value in options.items():
            if not hasattr(self, option):
                raise ValueError('Invalid option: {}'.format(option))
            setattr(self, option, value)

    def _make_figure(self):
        matplotlib.rcParams['xtick.direction'] = 'out'
        matplotlib.rcParams['ytick.direction'] = 'out'

        pyplot.figure(figsize=(12, 9))
        ax = pyplot.subplot(111)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Ensure ticks only on left and bottom, removing top and right ticks.
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

        args = {}
        fn = pyplot.plot

        if self.bars:
            fn = pyplot.bar
            args = {'width': self.bars_width}
        elif self.fill:
            fn = pyplot.fill_between

        fn(list(self.data.keys()), list(self.data.values()), **args)

        pyplot.title(self.title)
        pyplot.grid(self.grid)
        pyplot.xlabel(self.xlabel)
        pyplot.ylabel(self.ylabel)
        max_data = max(self.data.values())
        min_data = min(self.data.values())
        # Avoid trncating Y axis unless absolutely necessary.
        distance = max_data - min_data
        if distance > 0.01 * min_data:
            pyplot.ylim(0, max_data)
        else:
            pyplot.ylim(min_data - distance * 0.3, max_data + distance * 0.3)

        # Show full value in Y ticks, instead of using an offset.
        y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=False)
        ax.yaxis.set_major_formatter(y_formatter)

        pyplot.xlim(min(self.data.keys()), max(self.data.keys()))
        pyplot.xticks(fontsize=14)
        pyplot.yticks(fontsize=14)

    def show(self):
        self._make_figure()
        pyplot.show()
        pyplot.close()

    def save(self, path):
        self._make_figure()
        # Remove extraneous whitespace.
        pyplot.savefig(path, bbox_inches="tight")

if __name__ == '__main__':
    #Plot([100100, 100200, 100300, 100100, 100150, 100520, 100300]).show()
    Plot([0, 200, 300, 100, 150, 520, 300]).show()
    #Plot({'a': 100, 'b': 500}).show()
