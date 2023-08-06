"""Time series image analysis module for Python.
tsia is a Python package for time series analysis through images. It
aims to enable advanced diagnostic tools for time series through imaging
and visualization capabilities.
"""

from .plot import plot
from .markov import mtf as markov
from .network_graph import ng as network_graph
from .utils import tools as utils
from .diagnostics import histograms
from .diagnostics import profiling

__version__ = '0.1.13'
__all__ = [
    'markov', 'network_graph', 'plot', 'utils', 'histograms', 'profiling'
]