import gc

from pandas.io.sql import DataFrame, SQLDatabase, _convert_params

from .from_records import get_arrays_from_records
from .wrap_result import wrap_result


def db_read_query(
        self: SQLDatabase,
        sql,
        index_col=None,
        coerce_float=True,
        parse_dates=None,
        params=None,
        chunksize=None,
        downcast_types=None
):
    """Read SQL query into a DataFrame.

    Parameters
    ----------
    sql : string
        SQL query to be executed.
    index_col : string, optional, default: None
        Column name to use as index for the returned DataFrame object.
    coerce_float : boolean, default True
        Attempt to convert values of non-string, non-numeric objects (like
        decimal.Decimal) to floating point, useful for SQL result sets.
    params : list, tuple or dict, optional, default: None
        List of parameters to pass to execute method.  The syntax used
        to pass parameters is database driver dependent. Check your
        database driver documentation for which of the five syntax styles,
        described in PEP 249's paramstyle, is supported.
        Eg. for psycopg2, uses %(name)s so use params={'name' : 'value'}
    parse_dates : list or dict, default: None
        - List of column names to parse as dates.
        - Dict of ``{column_name: format string}`` where format string is
          strftime compatible in case of parsing string times, or is one of
          (D, s, ns, ms, us) in case of parsing integer timestamps.
        - Dict of ``{column_name: arg dict}``, where the arg dict
          corresponds to the keyword arguments of
          :func:`pandas.to_datetime` Especially useful with databases
          without native Datetime support, such as SQLite.
    chunksize : int, default None
        If specified, return an iterator where `chunksize` is the number
        of rows to include in each chunk.
    downcast_types : list, default: None
            List of column types to try to downcast. May be less then count of columns
            (In this case, the list will be expanded to uint8 to the number of columns)

    Returns
    -------
    DataFrame

    See Also
    --------
    read_sql_table : Read SQL database table into a DataFrame.
    read_sql

    """
    args = _convert_params(sql, params)

    result = self.execute(*args)
    columns = result.keys()
    if chunksize is not None:
        return db_query_iterator(
            result,
            chunksize,
            columns,
            index_col=index_col,
            coerce_float=coerce_float,
            parse_dates=parse_dates,
            downcast_types=downcast_types
        )
    else:
        raw_data = result.fetchall()

        data = [tuple(x) for x in raw_data]

        del raw_data
        gc.collect()

        frame = wrap_result(
            data,
            columns,
            index_col=index_col,
            coerce_float=coerce_float,
            parse_dates=parse_dates,
            downcast_types=downcast_types
        )
        return frame


def db_query_iterator(
        result, chunksize, columns, index_col=None, coerce_float=True, parse_dates=None, downcast_types=None
):
    """Return generator through chunked result set"""

    while True:
        raw_data = result.fetchmany(chunksize)
        if not raw_data:
            break
        else:
            data = [tuple(x) for x in raw_data]

            del raw_data
            gc.collect()

            arrays, columns, arr_columns = get_arrays_from_records(data, columns=columns, coerce_float=coerce_float, downcast_types=downcast_types)

            gc.collect()
            if downcast_types is not None:
                downcast_types = [array.dtype for array in arrays]
            yield arrays, columns, arr_columns
