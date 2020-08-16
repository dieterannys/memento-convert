from datetime import datetime
from dataclasses import dataclass
import sqlite3

import pandas as pd


@dataclass
class Field:
    uuid: str
    title: str
    type_code: str


@dataclass
class Value:
    field_uuid: str
    item_uuid: str
    value_str: str
    value_float: float
    value_int: int


@dataclass
class Item:
    uuid: str
    creation_date: datetime


@dataclass
class Library:
    uuid: str
    title: str


class MementoDB:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def query(self, query):
        return pd.read_sql(query, self.db)

    @property
    def tbl_library(self):
        return self.query("SELECT * FROM tbl_library")

    @property
    def tbl_library_item(self):
        return self.query("SELECT * FROM tbl_library_item")

    @property
    def tbl_flex_template(self):
        return self.query("SELECT * FROM tbl_flex_template")

    @property
    def tbl_flex_content2(self):
        return self.query("SELECT * FROM tbl_flex_content2")

    def get_libraries(self):
        return [
            Library(uuid=l.UUID, title=l.TITLE)
            for _, l in self.query(
                """
                SELECT *
                FROM tbl_library
                WHERE NOT REMOVED
            """
            ).iterrows()
        ]

    def get_fields(self, library_uuid):
        return [
            Field(uuid=f.UUID, title=f.title, type_code=f.type_code)
            for _, f in self.query(
                f"""
                SELECT *
                FROM tbl_flex_template
                WHERE LIB_UUID = '{library_uuid}'
                ORDER BY sortorder
            """
            ).iterrows()
        ]

    def get_items(self, library_uuid):
        return [
            Item(uuid=i.UUID, creation_date=i.creation_date)
            for _, i in self.query(
                f"""
                SELECT *
                FROM tbl_library_item
                WHERE LIB_UUID = '{library_uuid}'
                AND NOT REMOVED
            """
            ).iterrows()
        ]

    def get_values(self, library_uuid):
        return [
            Value(
                field_uuid=v.templateUUID,
                item_uuid=v.ownerUUID,
                value_str=None if pd.isnull(v.stringContent) else str(v.stringContent),
                value_float=None if pd.isnull(v.realContent) else float(v.realContent),
                value_int=None if pd.isnull(v.intContent) else int(v.intContent),
            )
            for _, v in self.query(
                f"""
                SELECT v.*
                FROM tbl_flex_content2 v
                INNER JOIN tbl_library_item i
                    ON v.ownerUUID = i.UUID
                    AND NOT i.REMOVED
                INNER JOIN tbl_flex_template f
                    ON v.templateUUID = f.UUID
                WHERE i.LIB_UUID = '{library_uuid}'
                AND f.LIB_UUID = '{library_uuid}'
            """
            ).iterrows()
        ]

    def close(self):
        self.db.close()
