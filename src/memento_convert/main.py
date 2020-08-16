import os
from datetime import datetime
import sqlite3
import argparse

import pandas as pd

from memento_convert.memento import MementoDB
from memento_convert.helper import normalize_name, coalesce, transform


def main():

    parser = argparse.ArgumentParser(description="Convert Memento Database db files to regular SQLite databases")
    parser.add_argument(
        "-i", "--input", type=str, help="input file (Memento Database db file)", default="memento.db",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="output file (SQLite db file)", default="extract.db",
    )
    args = parser.parse_args()

    memento_filename = args.input
    export_filename = args.output

    if os.path.exists(export_filename):
        os.remove(export_filename)

    with MementoDB(memento_filename) as memento, sqlite3.connect(export_filename) as export:

        for library in memento.get_libraries():

            fields = memento.get_fields(library.uuid)
            items = memento.get_items(library.uuid)
            values = memento.get_values(library.uuid)

            df = pd.DataFrame(columns=[f.uuid for f in fields], index=[i.uuid for i in items])

            for value in values:
                df.loc[value.item_uuid, value.field_uuid] = coalesce(
                    value.value_str, value.value_float, value.value_int
                )

            for field in fields:
                df[field.uuid] = transform(df[field.uuid], field.type_code)
                df.rename(columns={field.uuid: normalize_name(field.title)}, inplace=True)

            df["creation_date"] = None
            for item in items:
                df.loc[item.uuid, "creation_date"] = datetime.utcfromtimestamp(item.creation_date // 1000)

            df.sort_values("creation_date", inplace=True)
            df.reset_index(inplace=True, drop=True)

            df.to_sql(name=normalize_name(library.title), index=False, con=export)


if __name__ == "__main__":
    main()
