import numpy as np
import psutil
from memory_profiler import memory_usage
from pandas import DataFrame
from pandas.io.sql import _parse_date_columns

from .pandas_wrapper.from_records import prepare_arrays
from .pandas_wrapper.read_sql import stock_read_sql


def read_sql(sql,
             con,
             index_col=None,
             coerce_float=True,
             params=None,
             parse_dates=None,
             columns=None,
             chunksize=None,
             need_downcast=False,
             column_types=None,
             iterator=True,
             mapmem_th=0.9):
    """
    Extension of pandas.read_sql() for downcast column types of DataFrame.
    Parameters
    ----------
    sql : string or SQLAlchemy Selectable (select or text object)
        SQL query to be executed or a table name.
    con : SQLAlchemy connectable (engine/connection) or database string URI
        or DBAPI2 connection (fallback mode)
        Using SQLAlchemy makes it possible to use any DB supported by that
        library. If a DBAPI2 object, only sqlite3 is supported. The user is responsible
        for engine disposal and connection closure for the SQLAlchemy connectable. See
        `here <https://docs.sqlalchemy.org/en/13/core/connections.html>`_
    index_col : string or list of strings, optional, default: None
        Column(s) to set as index(MultiIndex).
    coerce_float : boolean, default True
        Attempts to convert values of non-string, non-numeric objects (like
        decimal.Decimal) to floating point, useful for SQL result sets.
    params : list, tuple or dict, optional, default: None
        List of parameters to pass to execute method.  The syntax used
        to pass parameters is database driver dependent. Check your
        database driver documentation for which of the five syntax styles,
        described in PEP 249's paramstyle, is supported.
        Eg. for psycopg2, uses %(name)s so use params={'name' : 'value'}.
    parse_dates : list or dict, default: None
        - List of column names to parse as dates.
        - Dict of ``{column_name: format string}`` where format string is
          strftime compatible in case of parsing string times, or is one of
          (D, s, ns, ms, us) in case of parsing integer timestamps.
        - Dict of ``{column_name: arg dict}``, where the arg dict corresponds
          to the keyword arguments of :func:`pandas.to_datetime`
          Especially useful with databases without native Datetime support,
          such as SQLite.
    columns : list, default: None
        List of column names to select from SQL table (only used when reading
        a table).
    chunksize : int, default: None
        If specified, return an iterator where `chunksize` is the
        number of rows to include in each chunk.
    need_downcast : bool, default: False
        To downcast column types or no
    column_types : list, default: None
        List of column types to try to downcast. May be less then count of columns
        (In this case, the list will be expanded to uint8 to the number of columns)
    iterator: bool, default: True
        To return iterator or full DataFrame when chunksize is not None.
    mapmem_th: float, default: 0.9
        Not Implemented

    Returns
    -------
    DataFrame or iterator
    See Also
    --------
    read_sql_table : Read SQL database table into a DataFrame.
    read_sql_query : Read SQL query into a DataFrame.
    """
    df = stock_read_sql(
        sql=sql,
        con=con,
        index_col=index_col,
        coerce_float=coerce_float,
        params=params,
        parse_dates=parse_dates,
        columns=columns,
        chunksize=chunksize,
        need_downcast=need_downcast,
        column_types=column_types
    )
    if chunksize is None:
        return df

    if iterator:
        def sql_iter(df):
            for iter_res in df:
                arrays, columns, arr_columns = iter_res
                frame = prepare_arrays(DataFrame, arrays, columns, arr_columns)

                frame = _parse_date_columns(frame, parse_dates)

                if index_col is not None:
                    frame.set_index(index_col, inplace=True)

                yield frame

        return sql_iter(df)

    mem_usage_before = memory_usage(max_usage=True)
    # mem_usage, result = memory_usage((next, (df,)), retval=True, max_usage=True)
    result = next(df)
    mem_usage = [0]
    max_chunksize = mem_usage[0] - mem_usage_before

    arrays = []
    for col in result[0]:
        arrays.append([col])

    columns = result[1]
    arr_columns = result[2]

    mem_used = (psutil.virtual_memory().used + max_chunksize) / psutil.virtual_memory().total
    need_mapmem = mem_used >= mapmem_th
    mem_usage_before = memory_usage(max_usage=True)

    for result in df:
        if need_mapmem:
            pass

        for i, col in enumerate(result[0]):
            arrays[i].append(np.array(col, dtype=col.dtype))

    arrays = [np.concatenate(col) for col in arrays]

    df = prepare_arrays(DataFrame, arrays, columns, arr_columns)

    df = _parse_date_columns(df, parse_dates)

    if index_col is not None:
        df.set_index(index_col, inplace=True)

    return df


def auto_read_sql(sql,
                  con,
                  index_col=None,
                  coerce_float=True,
                  params=None,
                  parse_dates=None,
                  columns=None,
                  chunksize=500000,
                  need_downcast=True,
                  column_types=None,
                  iterator=False,
                  mapmem_th=0.9):
    """
    Extension of read_sql() for optimal default params.
    Parameters
    ----------
    sql : string or SQLAlchemy Selectable (select or text object)
        SQL query to be executed or a table name.
    con : SQLAlchemy connectable (engine/connection) or database string URI
        or DBAPI2 connection (fallback mode)
        Using SQLAlchemy makes it possible to use any DB supported by that
        library. If a DBAPI2 object, only sqlite3 is supported. The user is responsible
        for engine disposal and connection closure for the SQLAlchemy connectable. See
        `here <https://docs.sqlalchemy.org/en/13/core/connections.html>`_
    index_col : string or list of strings, optional, default: None
        Column(s) to set as index(MultiIndex).
    coerce_float : boolean, default True
        Attempts to convert values of non-string, non-numeric objects (like
        decimal.Decimal) to floating point, useful for SQL result sets.
    params : list, tuple or dict, optional, default: None
        List of parameters to pass to execute method.  The syntax used
        to pass parameters is database driver dependent. Check your
        database driver documentation for which of the five syntax styles,
        described in PEP 249's paramstyle, is supported.
        Eg. for psycopg2, uses %(name)s so use params={'name' : 'value'}.
    parse_dates : list or dict, default: None
        - List of column names to parse as dates.
        - Dict of ``{column_name: format string}`` where format string is
          strftime compatible in case of parsing string times, or is one of
          (D, s, ns, ms, us) in case of parsing integer timestamps.
        - Dict of ``{column_name: arg dict}``, where the arg dict corresponds
          to the keyword arguments of :func:`pandas.to_datetime`
          Especially useful with databases without native Datetime support,
          such as SQLite.
    columns : list, default: None
        List of column names to select from SQL table (only used when reading
        a table).
    chunksize : int, default: 500000
        If specified, return an iterator where `chunksize` is the
        number of rows to include in each chunk.
    need_downcast : bool, default: True
        To downcast column types or no
    column_types : list, default: None
        Not Implemented
        List of column types to try to downcast. May be less then count of columns
    iterator: bool, default: True
        To return iterator or full DataFrame when chunksize is not None.
    mapmem_th: float, default: 0.9
        Not Implemented

    Returns
    -------
    DataFrame or iterator
    See Also
    --------
    read_sql : Read SQL database table into a DataFrame.
    """
    return read_sql(sql,
                    con,
                    index_col=index_col,
                    coerce_float=coerce_float,
                    params=params,
                    parse_dates=parse_dates,
                    columns=columns,
                    chunksize=chunksize,
                    need_downcast=need_downcast,
                    column_types=column_types,
                    iterator=iterator,
                    mapmem_th=mapmem_th)
