################################################################################
# Copyright (c) 2011-2019, National Research Foundation (Square Kilometre Array)
#
# Licensed under the BSD 3-Clause License (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy
# of the License at
#
#   https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

"""Data access library for data sets in the MeerKAT Visibility Format (MVF)."""

from __future__ import print_function, division, absolute_import
from future import standard_library
standard_library.install_aliases()  # noqa: E402
import future.utils
from past.builtins import basestring

import logging as _logging
import urllib.parse
import warnings

from .datasources import open_data_source
from .dataset import DataSet, WrongVersion
from .spectral_window import SpectralWindow
from .lazy_indexer import LazyTransform, dask_getitem
from .concatdata import ConcatenatedDataSet
from .h5datav1 import H5DataV1
from .h5datav2 import H5DataV2
from .h5datav3 import H5DataV3
from .visdatav4 import VisibilityDataV4


# Setup library logger and add a print-like handler used when no logging is configured
class _NoConfigFilter(_logging.Filter):
    """Filter which only allows event if top-level logging is not configured."""

    def filter(self, record):
        return 1 if not _logging.root.handlers else 0


_no_config_handler = _logging.StreamHandler()
_no_config_handler.setFormatter(_logging.Formatter(_logging.BASIC_FORMAT))
_no_config_handler.addFilter(_NoConfigFilter())
logger = _logging.getLogger(__name__)
logger.addHandler(_no_config_handler)

if future.utils.PY2:
    _PY2_WARNING = (
        "Python 2 has reached End-of-Life, and a future version of katdal "
        "will remove support for it. Please update your scripts to Python 3 "
        "as soon as possible."
    )
    warnings.warn(_PY2_WARNING, FutureWarning)


# Automatically added by katversion
__version__ = '0.17'

# -----------------------------------------------------------------------------
# -- Top-level functions passed on to the appropriate format handler
# -----------------------------------------------------------------------------

formats = [H5DataV3, H5DataV2, H5DataV1]


def _file_action(action, filename, *args, **kwargs):
    """Perform action on data file using the appropriate format class.

    Parameters
    ----------
    action : string
        Name of method to call on format class
    filename : string
        Data file name
    args, kwargs : extra parameters to method (optional)

    Returns
    -------
    result : object
        Result of action

    """
    for format in formats:
        try:
            result = getattr(format, action)(filename, *args, **kwargs)
            break
        except WrongVersion:
            continue
    else:
        raise WrongVersion("File '%s' has unknown data file format or version"
                           % (filename,))
    return result


def open(filename, ref_ant='', time_offset=0.0, **kwargs):
    """Open data file(s) with loader of the appropriate version.

    Parameters
    ----------
    filename : string or sequence of strings
        Data file name or list of file names
    ref_ant : string, optional
        Name of reference antenna (default is first antenna in use)
    time_offset : float, optional
        Offset to add to all timestamps, in seconds
    kwargs : dict, optional
        Extra keyword arguments are passed on to underlying accessor class:

        mode (string, optional)
            [H5DataV*] File opening mode (e.g. 'r+' to open file in write mode)
        quicklook (bool)
            [H5DataV2] True if synthesised timestamps should be used to
            partition data set even if real timestamps are irregular, thereby
            avoiding the slow loading of real timestamps at the cost of
            slightly inaccurate label borders

    Returns
    -------
    data : :class:`DataSet` object
        Object providing :class:`DataSet` interface to file(s)

    """
    filenames = [filename] if isinstance(filename, basestring) else filename
    datasets = []
    for f in filenames:
        # V4 RDB file or live telstate with optional URL-style query string
        parsed = urllib.parse.urlsplit(f)
        if parsed.path.endswith('.rdb') or parsed.scheme != '':
            dataset = VisibilityDataV4(open_data_source(f, **kwargs),
                                       ref_ant, time_offset, **kwargs)
        else:
            dataset = _file_action('__call__', f, ref_ant, time_offset, **kwargs)
        datasets.append(dataset)
    return datasets[0] if isinstance(filename, basestring) else \
        ConcatenatedDataSet(datasets)


def get_ants(filename):
    """Quick look function to get the list of antennas in a data file.

    Parameters
    ----------
    filename : string
        Data file name

    Returns
    -------
    antennas : list of :class:`katpoint.Antenna` objects

    """
    return _file_action('_get_ants', filename)


def get_targets(filename):
    """Quick look function to get the list of targets in a data file.

    Parameters
    ----------
    filename : string
        Data file name

    Returns
    -------
    targets : :class:`katpoint.Catalogue` object
        All targets in file

    """
    return _file_action('_get_targets', filename)
