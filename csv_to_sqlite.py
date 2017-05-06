#!/usr/bin/env python

"""converts csv files to sqlite db"""
import csv
import sqlite3
import argparse
import os.path
import glob


def proc_args():
    """used to setup command line arguments"""
    parser = argparse.ArgumentParser(
        description="Converts csv files to sqlite db",)
    parser.add_argument(
        "csv_path",
        nargs="+",
        help=(
            "path(s) to csv file(s) to convert, "
            "wildcards and directories are supported, "
            "use a space to separate multiple paths"))
    parser.add_argument(
        "-o",
        "--out_db",
        help=(
            "name and path of the sqlite database, "
            "only used if mode is either single or multi_table"
            " it's ignored in multi_db mode. "
            "Default is ./out_db.sqlite"),
        default="out.sqlite")
    parser.add_argument(
        "-t",
        "--table",
        help=(
            "name of the table into wich the rows will be inserted, "
            "if provided in multi table mode a progressive number is "
            "appended to each table. Default is export in single mode "
            "otherwise it's [csv_file_name]"))
    parser.add_argument(
        "-c",
        "--columns",
        nargs="+",
        help=(
            "space separated names of the columns "
            "to be created in the provided table. "
            "Default behaviour is to use the "
            "first line in the csv file)"))
    parser.add_argument(
        "-m",
        "--mode",
        choices=[
            "single",
            "multi_table",
            "multi_db"],
        help=(
            "mode to use\nsingle: only one database file is created and "
            "one table\nmulti_table: one db and multiple tables\n"
            "multi_db: multiple db files, each one with a single table.\n"
            "Default is single"),
        default="single")
    parser.add_argument(
        "-d",
        "--delimiter",
        help=(
            "the character used to separate values in the "
            "csv file. Default is comma ','"),
        default=",")
    parser.add_argument(
        "-a",
        "--append",
        action="store_true",
        help=(
            "if set, the script will append some empty strings "
            "in case the length of line in the csv doesn't "
            "match the number of columns provided"))

    return parser.parse_args()


def process_csv(csv_file, args, count):
    """used to process csv's in single db mode"""
    csv_data = read_csv_data(csv_file, args.delimiter)
    columns = get_columns(args.columns, csv_data)
    table = get_table_name_for_mode(args.table, csv_file, args.mode, count)
    out_db = get_out_db_name_for_mode(args.out_db, csv_file, args.mode)

    con = sqlite3.connect(out_db)
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS '{}' ({})".format(
            table, ",".join(columns)))
    insert_query = "INSERT INTO '{}' ({}) VALUES ({})".format(
        table, ",".join(columns), ",".join(["?" for col in columns]))
    if args.append:
        fix_data_length(csv_data, len(columns))
    cur.executemany(insert_query, csv_data)
    con.commit()
    con.close()


def fix_data_length(data, n_col):
    """appends empty strings to data till line length matches
    the number of columns"""
    for line in data:
        for _ in range(0, n_col - len(line)):
            line.append("")


def get_file_name(file):
    """returns the basename of the file passed without extension"""
    return os.path.splitext(os.path.basename(file))[0]


def read_csv_data(csv_file, delimiter):
    """returns a list containing the data found in the csv_file"""
    with open(csv_file, "r") as f_in:
        return list(csv.reader(f_in, delimiter=delimiter))


def get_columns(columns, csv_data):
    """returns a list containing columns names"""
    if columns is None:
        columns = csv_data.pop(0)
    elif len(columns) < len(csv_data[0]):
        columns += append_default_columns(len(columns), len(csv_data[0]))

    return [c.replace(" ", "_") for c in columns]


def get_table_name_for_mode(table, csv_file, mode, count):
    """return the proper name of the table to insert the data in
    depending on the mode choosen
    """
    if table is None and mode != "single":
        return get_file_name(csv_file)
    elif table is None and mode == "single":
        return "export"
    elif mode == "multi_table":
        return table + "_" + str(count)
    else:
        return table


def get_out_db_name_for_mode(out_db, csv_file, mode):
    """return the proper name of the outuput db depending
    on the mode choosen
    """
    if mode == "multi_db":
        return get_file_name(csv_file) + ".sqlite"
    else:
        return out_db


def append_default_columns(start, num):
    """appends num string to a list as col_[index]"""
    columns = []

    for i in range(start, num):
        columns.append("col_" + str(i + 1))

    return columns


def sanitize_paths(args_paths):
    """used to resolve wildcards in passed paths,
    needed for Windows and in case wildcards are escaped
    """
    sanitized_paths = []
    for path in args_paths:
        if "*" or "?" in path:  # Windows shells do not expand wildcards
            sanitized_paths.extend(glob.glob(path))
        else:
            sanitized_paths.append(path)

    return sanitized_paths


def main():
    """main"""
    args = proc_args()
    count = 0

    arg_paths = sanitize_paths(args.csv_path)

    for csv_path in arg_paths:  # iterate through passed paths
        if os.path.isdir(csv_path):
            csv_path += "/*"
        for csv_file in glob.iglob(csv_path):
            if csv_file.endswith(".csv"):
                print("converting ", csv_file, end='')
                count += 1
                process_csv(csv_file, args, count)
                print(" -> done")

    if count > 0:
        print("Operation completed, converted", count, "files")
    else:
        print("No files where converted, check arguments")


if __name__ == '__main__':
    main()
