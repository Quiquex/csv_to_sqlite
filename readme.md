# Csv to sqlite
This script converts one or multiple csv files to sqlite 3 database(s).
It's kinda crude and written in haste since we needed it at my work place (not a coder)
and a quick look around didn't satisfy our specific needs.
It has not been thoroughly tested so use it at your own risk.
Have a look at [sqlitebiter](https://github.com/thombashi/sqlitebiter) if you want more features.

## Purpose
We had to reorganize and search around several thousaunds csv files, but we had the
following issues:
- csv files were spread around in many directories
- some csv files had no header row
- in some files number of columns wasn't consistent in all the rows
- some csv files needed to be copied in a single table each one
- many others needed to be inserted in the same table
- the script needed to be used from both Windows and Linux machines
- some csv were not comma separated but used another specific locale delimiter

All of the above lead to the creation of this script.

## Usage
```
csv_to_sqlite.py [-h] [-o OUT_DB] [-t TABLE] [-c COLUMNS [COLUMNS ...]]
                        [-m {single,multi_table,multi}] [-d DELIMITER]
                        [-a APPEND]
                        csv_path [csv_path ...]

Converts csv files to sqlite db

positional arguments:
  csv_path              path(s) to csv file(s) to convert, wildcards and
                        directories are supported, use a space to separate
                        multiple paths

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_DB, --out_db OUT_DB
                        name and path of the sqlite database, only used if
                        mode is either single or multi_table it's ignored in
                        multi_db mode. Default is ./out_db.sqlite
  -t TABLE, --table TABLE
                        name of the table into wich the rows will be inserted,
                        if provided in multi table mode a progressive number
                        is appended to each table. Default is export in single
                        mode otherwise it's [csv_file_name]
  -c COLUMNS [COLUMNS ...], --columns COLUMNS [COLUMNS ...]
                        space separated names of the columns to be created in
                        the provided table. Default behaviour is to use the
                        first line in the csv file)
  -m {single,multi_table,multi_db}, --mode {single,multi_table,multi_db}
                        mode to use single: only one database file is created
                        and one table multi_table: one db and multiple tables
                        multi_db: multiple db files, each one with a single
                        table. Default is single
  -d DELIMITER, --delimiter DELIMITER
                        the character used to separate values in the csv file.
                        Default is comma ','
  -a, --append          if set, the script will append some empty strings in
                        case the length of line in the csv doesn't match the
                        number of columns provided
```

## Requirements
Python 3.4+

## License 
MIT License
