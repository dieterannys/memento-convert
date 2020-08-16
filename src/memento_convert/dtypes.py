from datetime import datetime
from dataclasses import dataclass
from typing import Callable


@dataclass
class DType:
    memento_type_code: str = None
    pandas_dtype: str = "object"
    sqlite_type: str = "TEXT"
    transform_func: Callable = lambda x: x


dtypes = [
    DType(
        memento_type_code="ft_date",
        sqlite_type="DATE",
        transform_func=lambda x: datetime.utcfromtimestamp(int(x) // 1000).strftime("%Y-%m-%d"),
    ),
    DType(memento_type_code="ft_int", pandas_dtype="int32", sqlite_type="INTEGER"),
]


dtypes_map = {t.memento_type_code: t for t in dtypes}


default_dtype = DType()
