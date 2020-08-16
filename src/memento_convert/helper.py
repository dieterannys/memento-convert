import re

from memento_convert.dtypes import dtypes_map, default_dtype


def normalize_name(s):
    return re.sub(r"[\-_\s]", "_", s.lower())


def coalesce(*elements):
    for element in elements:
        if element is None:
            continue
        return element


def transform(column, memento_type_code):
    return column.apply(dtypes_map.get(memento_type_code, default_dtype).transform_func).astype(
        dtypes_map.get(memento_type_code, default_dtype).pandas_dtype
    )
