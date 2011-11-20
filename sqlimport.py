#!/usr/bin/env python

import csv
import sqlite3 as sqlite

def _to_sql(value):
    try:
        return float(value)
    except ValueError:
        return value


def main():
    data_path = "../data_atrade/training.csv"
    con = sqlite.connect("data.sqlite")
    cursor = con.cursor()

    with open(data_path, "rb") as input:
        reader = csv.reader(input, delimiter=",")
        header = reader.next()
        placeholders = ",".join("?" * len(header))
        insert_sql = "insert into train values (%s)" % placeholders

        cursor.execute("create table train (%s)" % ",".join(header))
        for i, row in enumerate(reader):
            if i % 1000 == 0:
                print i
            values = [_to_sql(v) for v in row]
            con.execute(insert_sql, values)

    con.commit()
    con.close()


main()
