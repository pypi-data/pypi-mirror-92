import gc
import warnings

from pandas.core.frame import (
    ensure_index,
    DataFrame,
    arrays_to_mgr
)

from .to_arrays import to_arrays


def get_arrays_from_records(
        data,
        columns=None,
        coerce_float=False,
        downcast_types=None,
):
    """
    Convert structured or record ndarray to DataFrame.

    Parameters
    ----------
    data : ndarray (structured dtype), list of tuples, dict, or DataFrame
    columns : sequence, default None
        Column names to use. If the passed data do not have names
        associated with them, this argument provides names for the
        columns. Otherwise this argument indicates the order of the columns
        in the result (any names not found in the data will become all-NA
        columns)
    downcast_types : list, default: None
            List of column types to try to downcast. May be less then count of columns
            (In this case, the list will be expanded to uint8 to the number of columns)
    coerce_float : boolean, default False
        Attempt to convert values of non-string, non-numeric objects (like
        decimal.Decimal) to floating point, useful for SQL result sets

    Returns
    -------
    DataFrame
    """
    # Make a copy of the input columns so we can modify it
    if columns is not None:
        columns = ensure_index(columns)

    arrays, arr_columns = to_arrays(data, columns, coerce_float=coerce_float, downcast_types=downcast_types)
    gc.collect()
    return arrays, columns, arr_columns


def prepare_arrays(cls, arrays, columns, arr_columns):
    arr_columns = ensure_index(arr_columns)
    if columns is not None:
        columns = ensure_index(columns)
    else:
        warnings.warn("This method has not been tested. Please inform development departament about this!")
        columns = arr_columns

    result_index = None
    mgr = arrays_to_mgr(arrays, arr_columns, result_index, columns)

    return cls(mgr)
