import re

from sqlalchemy import util
from sqlalchemy.sql import compiler, sqltypes
from sqlalchemy.sql.type_api import TypeEngine

# https://trino.io/docs/current/language/reserved.html
RESERVED_WORDS = {
    "alter",
    "and",
    "as",
    "between",
    "by",
    "case",
    "cast",
    "constraint",
    "create",
    "cross",
    "cube",
    "current_date",
    "current_path",
    "current_role",
    "current_time",
    "current_timestamp",
    "current_user",
    "deallocate",
    "delete",
    "describe",
    "distinct",
    "drop",
    "else",
    "end",
    "escape",
    "except",
    "execute",
    "exists",
    "extract",
    "false",
    "for",
    "from",
    "full",
    "group",
    "grouping",
    "having",
    "in",
    "inner",
    "insert",
    "intersect",
    "into",
    "is",
    "join",
    "left",
    "like",
    "localtime",
    "localtimestamp",
    "natural",
    "normalize",
    "not",
    "null",
    "on",
    "or",
    "order",
    "outer",
    "prepare",
    "recursive",
    "right",
    "rollup",
    "select",
    "table",
    "then",
    "true",
    "uescape",
    "union",
    "unnest",
    "using",
    "values",
    "when",
    "where",
    "with",
}

# https://trino.io/docs/current/language/types.html
_type_map = {
    # === Boolean ===
    'boolean': sqltypes.BOOLEAN,

    # === Integer ===
    'tinyint': sqltypes.SMALLINT,
    'smallint': sqltypes.SMALLINT,
    'integer': sqltypes.INTEGER,
    'bigint': sqltypes.BIGINT,

    # === Floating-point ===
    'real': sqltypes.FLOAT,
    'double': sqltypes.FLOAT,

    # === Fixed-precision ===
    'decimal': sqltypes.DECIMAL,

    # === String ===
    'varchar': sqltypes.VARCHAR,
    'char': sqltypes.CHAR,
    'varbinary': sqltypes.VARBINARY,
    'json': sqltypes.JSON,

    # === Date and time ===
    'date': sqltypes.DATE,
    'time': sqltypes.Time,
    'time with time zone': sqltypes.Time,
    'timestamp': sqltypes.TIMESTAMP,
    'timestamp with time zone': sqltypes.TIMESTAMP,

    # 'interval year to month': IntervalOfYear,  # TODO
    'interval day to second': sqltypes.Interval,

    # === Structural ===
    'array': sqltypes.ARRAY,
    # 'map': MAP
    # 'row': ROW

    # === Mixed ===
    # 'ipaddress': IPADDRESS
    # 'uuid': UUID,
    # 'hyperloglog': HYPERLOGLOG,
    # 'p4hyperloglog': P4HYPERLOGLOG,
    # 'qdigest': QDIGEST,
    # 'tdigest': TDIGEST,
}


def parse_sqltype(type_str: str, column: str) -> TypeEngine:
    type_str = type_str.lower()
    m = re.match(r'^([\w\s]+)(?:\(([\d,\s]*)\))?', type_str)
    if m is None:
        util.warn(f"Could not parse type name '{type_str}'")
        return sqltypes.NULLTYPE
    type_name, type_opts = m.groups()  # type: str, str
    type_name = type_name.strip()
    if type_name not in _type_map:
        util.warn(f"Did not recognize type '{type_name}' of column '{column}'")
        return sqltypes.NULLTYPE
    type_class = _type_map[type_name]
    type_args = [int(o.strip()) for o in type_opts.split(',')] if type_opts else []
    if type_name in ('time', 'timestamp'):
        type_kwargs = dict(timezone=type_str.endswith("with time zone"))
        # TODO: handle time/timestamp(p) precision
        return type_class(**type_kwargs)
    if type_name in ('array', 'map', 'row'):
        # TODO
        return sqltypes.NULLTYPE
    return type_class(*type_args)


class TrinoSQLCompiler(compiler.SQLCompiler):
    pass


class TrinoDDLCompiler(compiler.DDLCompiler):
    pass


class TrinoTypeCompiler(compiler.GenericTypeCompiler):
    pass


class TrinoIdentifierPreparer(compiler.IdentifierPreparer):
    reserved_words = RESERVED_WORDS
