# -*- coding: utf-8 -*-
# flake8: noqa

from pkg_resources import DistributionNotFound, get_distribution
from py_spm._channel import Channel
from py_spm._data import Data
from py_spm._event import Event
from py_spm._meeg import MEEG
from py_spm._trial import Trial

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
