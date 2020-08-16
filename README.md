# Memento Database Converter

## Introduction

On the go, I use the excellent [Memento Database](https://mementodatabase.com) application for Android for keeping track of things, but I was in need of a way to easily pull out an SQLite3 database with my data so I could further process it on my computer. This is a *very* preliminary version of a conversion tool for this purpose.

## Installation

Git clone the repo and install from the root folder using the following command:

```bash
pip install .
```

## Usage

In the Memento Database application, make a backup from the Settings menu, pull the backup file to the computer and unzip.

Execute the command, example:

```bash
memento-convert -i memento.db -o extract.db
```

The resulting file is a SQLite3 database containing your libraries as regular tables.
