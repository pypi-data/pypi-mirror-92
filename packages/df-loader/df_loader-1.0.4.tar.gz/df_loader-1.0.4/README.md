# df_loader
Модуль, реализующий функции `read_sql()` и `auto_read_sql()`. 

Данные функции позволяют получить из базы данных DataFrame, который
использовует существенно меньше оперативной памяти. Чем больше 
в данных числовых столбцов, тем больше экономия памяти. Например,
DataFrame, полученный из таблицы ``promocodes.dbo.recsys_wgh2_train_nmf_coef``,
будет весить на 64% меньше.

`read_sql`  копирует функционал `pandas.read_sql()` и интерфейс метода полностью
 совместим с ним. Однако, имеет дополнительные опциональные параметры:
- **need_downcast=False**
- **iterator=True**

`auto_read_sql` является оберткой вокруг `read_sql` с измененными параметрами
по умолчанию:
- **chunksize=500000**
- **need_downcast=True**
- **iterator=False**


## Примеры
Получение DataFrame целиком, как `pd.read_sql()`
````python
from df_loader import read_sql

df = read_sql(query, con)
````

Получение итератора Dataframe чанками, как `pd.read_sql()`
````python
from df_loader import read_sql

iterator = read_sql(query, con, chunksize=20000)
````

Получение Dataframe целиком, но с оптимизированными типами
````python
from df_loader import read_sql

df = read_sql(query, con, need_downcast=True)
````

Получение итератора Dataframe чанками, с оптимизированными типами
````python
from df_loader import read_sql

iterator = read_sql(query, con, chunksize=20000, need_downcast=True)
````

Получение Dataframe (не итератора!) с оптимизированными типами, загруженного чанками
````python
from df_loader import read_sql

df = read_sql(query, con, chunksize=20000, need_downcast=True, iterator=False)
````

Тоже самое, но с помощью `auto_read_sql`
````python
from df_loader import auto_read_sql

df = auto_read_sql(query, con)
````


## Рекомендация
Для датасетов, которые занимают половину доступной памяти и более, 
настоятельно рекомендуется использовать загрузку чанками, тк прежде чем сдаункастить 
типы, в память будет загружен DataFrame средствами самого пандас (т.е. с жирными типами)


## sql_load interface
````python
from df_loader import read_sql

read_sql(sql,
         con,
         index_col=None,
         coerce_float=True,
         params=None,
         parse_dates=None,
         columns=None,
         chunksize=None,
         need_downcast=False,
         column_types=None,
         iterator=True)
````

#### sql
string or SQLAlchemy Selectable (select or text object) SQL query to be executed or a table name.

#### con
SQLAlchemy connectable (engine/connection) or database string URI or DBAPI2 connection (fallback mode).

Using SQLAlchemy makes it possible to use any DB supported by that
library. If a DBAPI2 object, only sqlite3 is supported. The user is responsible
for engine disposal and connection closure for the SQLAlchemy connectable. 

#### index_col: string or list of str, default: None
Column(s) to set as index(MultiIndex).

#### coerce_float: boolean, default True
Attempts to convert values of non-string, non-numeric objects (like
decimal.Decimal) to floating point, useful for SQL result sets.

#### params: list, tuple or dict, optional, default: None
List of parameters to pass to execute method.  The syntax used
to pass parameters is database driver dependent. Check your
database driver documentation for which of the five syntax styles,
described in PEP 249's paramstyle, is supported.

Eg. for psycopg2, uses %(name)s so use params={'name' : 'value'}.

#### parse_dates: list or dict, default: None
- List of column names to parse as dates.
- Dict of ``{column_name: format string}`` where format string is
  strftime compatible in case of parsing string times, or is one of
  (D, s, ns, ms, us) in case of parsing integer timestamps.
- Dict of ``{column_name: arg dict}``, where the arg dict corresponds
  to the keyword arguments of :func:`pandas.to_datetime`
  Especially useful with databases without native Datetime support,
  such as SQLite.

#### columns: list, default: None
List of column names to select from SQL table (only used when reading
a table).


#### chunksize: int, default None
Если задан, то:
1) **если iterator=True**, вернет вернет итератор
2) **если iterator=False**, чанками загрузит датафреймы, 
объединит их в один и вернет его как результат.


#### need_downcast: bool, default False
Флаг, устанавливающий нужна оптимизация памяти или нет.

Для каждого столбца проверяется лежат ли его значения внутри 
uint8 -> uint16 -> ... -> int8 -> ... - > int64 -> float16 -> ... -> float64 -> object.

Если загрузка чанками, то учитываются типы столбцов из предыдущих чанков и приводятся к наибольшему.


#### column_types: list, default None
Not Implemented


#### iterator: bool, default True
Флаг, устанавливающий должен вернуться итератор или уже собранный из 
чанков DataFrame (если задан chunksize).