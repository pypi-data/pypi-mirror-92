from pandas import DataFrame
from pandas.io.sql import SQLTable, _parse_date_columns

from .from_records import get_arrays_from_records, prepare_arrays


def wrap_result(data, columns, index_col=None, coerce_float=True, parse_dates=None, downcast_types=None):
    """Wrap result set of query in a DataFrame."""

    arrays, columns, arr_columns = get_arrays_from_records(data, columns=columns, coerce_float=coerce_float,
                                                           downcast_types=downcast_types)

    frame = prepare_arrays(DataFrame, arrays, columns, arr_columns)
    frame = _parse_date_columns(frame, parse_dates)

    if index_col is not None:
        frame.set_index(index_col, inplace=True)

    return frame


def table_wrap_result(self: SQLTable, data, columns=None, coerce_float=True, parse_dates=None, downcast_types=None):
    arrays, columns, arr_columns = get_arrays_from_records(
        data, columns=columns, coerce_float=coerce_float, downcast_types=downcast_types
    )
    self.frame = prepare_arrays(DataFrame, arrays, columns, arr_columns)

    self._harmonize_columns(parse_dates=parse_dates)

    if self.index is not None:
        self.frame.set_index(self.index, inplace=True)
