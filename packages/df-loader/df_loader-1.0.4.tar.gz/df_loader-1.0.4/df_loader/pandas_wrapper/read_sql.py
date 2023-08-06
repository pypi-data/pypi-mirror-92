from pandas.io.sql import pandasSQL_builder, SQLiteDatabase

from .read_db import db_read_query
from .read_sqlite import sqlite_read_query
from .read_table import db_read_table


def stock_read_sql(sql,
                   con,
                   index_col=None,
                   coerce_float=True,
                   params=None,
                   parse_dates=None,
                   columns=None,
                   chunksize=None,
                   need_downcast=False,
                   column_types=None
                   ):
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

    Returns
    -------
    DataFrame or iterator
    See Also
    --------
    read_sql_table : Read SQL database table into a DataFrame.
    read_sql_query : Read SQL query into a DataFrame.
    """
    pandas_sql = pandasSQL_builder(con)

    downcast_types = None
    if need_downcast:
        if column_types is None:
            downcast_types = []
        else:
            downcast_types = column_types

    if isinstance(pandas_sql, SQLiteDatabase):
        pandas_sql.sqlite_read_query = sqlite_read_query.__get__(pandas_sql)
        return pandas_sql.sqlite_read_query(
            sql,
            index_col=index_col,
            params=params,
            coerce_float=coerce_float,
            parse_dates=parse_dates,
            chunksize=chunksize,
            downcast_types=downcast_types
        )

    try:
        _is_table_name = pandas_sql.has_table(sql)
    except Exception:
        # using generic exception to catch errors from sql drivers (GH24988)
        _is_table_name = False

    if _is_table_name:
        pandas_sql.meta.reflect(only=[sql])
        pandas_sql.db_read_table = db_read_table.__get__(pandas_sql)
        return pandas_sql.db_read_table(
            sql,
            index_col=index_col,
            coerce_float=coerce_float,
            parse_dates=parse_dates,
            columns=columns,
            chunksize=chunksize,
            downcast_types=downcast_types
        )
    else:
        pandas_sql.db_read_query = db_read_query.__get__(pandas_sql)
        return pandas_sql.db_read_query(
            sql,
            index_col=index_col,
            params=params,
            coerce_float=coerce_float,
            parse_dates=parse_dates,
            chunksize=chunksize,
            downcast_types=downcast_types
        )
