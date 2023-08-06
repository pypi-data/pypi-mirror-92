import gc
import warnings

import numpy as np
from numpy import uint8
from pandas._libs import lib
from pandas.core.indexes import base as ibase
from pandas.core.internals.construction import (
    maybe_cast_to_datetime,
)

from df_loader.pandas_sql_loader.downcast import downcast


def to_arrays(data, columns, coerce_float=False, dtype=None, downcast_types=None):
    """
    Return list of arrays, columns.
    """
    if not len(data):
        if isinstance(data, np.ndarray):
            warnings.warn("This method has not been tested. Please inform development departament about this!")
            columns = data.dtype.names
            if columns is not None:
                return [[]] * len(columns), columns
        return [], []  # columns if columns is not None else []

    # last ditch effort
    # data = [tuple(x) for x in data]

    if downcast_types is not None:
        len_downcast = len(downcast_types)
        len_data = len(data[0])
        if len_downcast < len_data:
            new_types = [uint8] * (len_data - len_downcast)
            downcast_types += new_types
    return _list_to_arrays(data, columns, coerce_float=coerce_float, dtype=dtype, downcast_types=downcast_types)


def _list_to_arrays(data, columns, coerce_float=False, dtype=None, downcast_types=None):
    if len(data) > 0 and isinstance(data[0], tuple):
        content = list(lib.to_object_array_tuples(data).T)
    else:
        # list of lists
        content = list(lib.to_object_array(data).T)
    # gh-26429 do not raise user-facing AssertionError
    data.clear()
    gc.collect()

    try:
        result = _convert_object_array(
            content, columns, dtype=dtype, coerce_float=coerce_float, downcast_types=downcast_types
        )
    except AssertionError as e:
        warnings.warn("This method has not been tested. Please inform development departament about this!")
        raise ValueError(e) from e

    return result


def _convert_object_array(content, columns, coerce_float=False, dtype=None, downcast_types=None):
    if columns is None:
        warnings.warn("This method has not been tested. Please inform development departament about this!")
        columns = ibase.default_index(len(content))
    else:
        if len(columns) != len(content):  # pragma: no cover
            # caller's responsibility to check for this...
            raise AssertionError(
                "{col:d} columns passed, passed data had "
                "{con} columns".format(col=len(columns), con=len(content))
            )

    # provide soft conversion of object dtypes
    def convert(arr, downcast_ind):
        if dtype != object and dtype != np.object:
            arr = lib.maybe_convert_objects(arr, try_float=coerce_float)
            if downcast_types is not None and len(downcast_types):
                arr = downcast(arr, downcast_types[downcast_ind])
            arr = maybe_cast_to_datetime(arr, dtype)
        return arr

    arrays = [convert(arr, i) for i, arr in enumerate(content)]
    return arrays, columns
