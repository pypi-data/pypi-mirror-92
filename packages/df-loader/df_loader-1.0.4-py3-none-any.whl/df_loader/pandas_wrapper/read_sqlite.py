import gc
import warnings

from pandas.io.sql import SQLiteDatabase, _convert_params

from .from_records import get_arrays_from_records
from .wrap_result import wrap_result


def sqlite_read_query(
        self: SQLiteDatabase,
        sql,
        index_col=None,
        coerce_float=True,
        params=None,
        parse_dates=None,
        chunksize=None,
        downcast_types=None
):
    args = _convert_params(sql, params)
    cursor = self.execute(*args)
    columns = [col_desc[0] for col_desc in cursor.description]

    if chunksize is not None:
        return sqlite_query_iterator(
            cursor,
            chunksize,
            columns,
            index_col=index_col,
            coerce_float=coerce_float,
            parse_dates=parse_dates,
            downcast_types=downcast_types
        )
    else:
        data = self._fetchall_as_list(cursor)
        cursor.close()

        frame = wrap_result(
            data,
            columns,
            index_col=index_col,
            coerce_float=coerce_float,
            parse_dates=parse_dates,
            downcast_types=downcast_types
        )
        return frame


def sqlite_query_iterator(
    cursor, chunksize, columns, index_col=None, coerce_float=True, parse_dates=None, downcast_types=None
):
    """Return generator through chunked result set"""

    while True:
        raw_data = cursor.fetchmany(chunksize)
        if type(raw_data) == tuple:
            warnings.warn("This method has not been tested. Please inform development departament about this!")
            raw_data = list(raw_data)
        if not raw_data:
            cursor.close()
            break
        else:
            data = [tuple(x) for x in raw_data]

            del raw_data
            gc.collect()

            arrays, columns, arr_columns = get_arrays_from_records(data, columns=columns, coerce_float=coerce_float,
                                                                   downcast_types=downcast_types)
            gc.collect()
            if downcast_types is not None:
                downcast_types = [array.dtype for array in arrays]
            yield arrays, columns, arr_columns

