import gc

from pandas.core.api import DataFrame
from pandas.io.sql import SQLTable

from .from_records import get_arrays_from_records
from .wrap_result import table_wrap_result


def db_read_table(
        self,
        table_name,
        index_col=None,
        coerce_float=True,
        parse_dates=None,
        columns=None,
        schema=None,
        chunksize=None,
        downcast_types=None
):
    """Read SQL database table into a DataFrame.

    Parameters
    ----------
    table_name : string
        Name of SQL table in database.
    index_col : string, optional, default: None
        Column to set as index.
    coerce_float : boolean, default True
        Attempts to convert values of non-string, non-numeric objects
        (like decimal.Decimal) to floating point. This can result in
        loss of precision.
    parse_dates : list or dict, default: None
        - List of column names to parse as dates.
        - Dict of ``{column_name: format string}`` where format string is
          strftime compatible in case of parsing string times, or is one of
          (D, s, ns, ms, us) in case of parsing integer timestamps.
        - Dict of ``{column_name: arg}``, where the arg corresponds
          to the keyword arguments of :func:`pandas.to_datetime`.
          Especially useful with databases without native Datetime support,
          such as SQLite.
    columns : list, default: None
        List of column names to select from SQL table.
    schema : string, default None
        Name of SQL schema in database to query (if database flavor
        supports this).  If specified, this overwrites the default
        schema of the SQL database object.
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
    pandas.read_sql_table
    SQLDatabase.read_query

    """
    table = SQLTable(table_name, self, index=index_col, schema=schema)
    table.myread = read.__get__(table)
    return table.myread(
        coerce_float=coerce_float,
        parse_dates=parse_dates,
        columns=columns,
        chunksize=chunksize,
        downcast_types=downcast_types
    )


def read(self: SQLTable, coerce_float=True, parse_dates=None, columns=None, chunksize=None, downcast_types=None):
    if columns is not None and len(columns) > 0:
        from sqlalchemy import select

        cols = [self.table.c[n] for n in columns]
        if self.index is not None:
            [cols.insert(0, self.table.c[idx]) for idx in self.index[::-1]]
        sql_select = select(cols)
    else:
        sql_select = self.table.select()

    result = self.pd_sql.execute(sql_select)
    column_names = result.keys()

    if chunksize is not None:
        self.table_query_iterator = table_query_iterator.__get__(self)
        return self.table_query_iterator(
            result,
            chunksize,
            column_names,
            coerce_float=coerce_float,
            parse_dates=parse_dates,
            downcast_types=downcast_types
        )
    else:
        data = result.fetchall()
        self.table_wrap_result = table_wrap_result.__get__(self)
        self.table_wrap_result(data,
                               column_names,
                               coerce_float=coerce_float,
                               parse_dates=parse_dates,
                               downcast_types=downcast_types)

        return self.frame


def table_query_iterator(
        self: SQLTable, result, chunksize, columns, coerce_float=True, parse_dates=None, downcast_types=None
):
    """Return generator through chunked result set."""

    while True:
        raw_data = result.fetchmany(chunksize)
        if not raw_data:
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
