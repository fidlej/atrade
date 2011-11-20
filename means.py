#!/usr/bin/env python
"""Generates changes.pickle.
The file will contain sums of bid and ask changes.
Different sums are provided for different groups of rows.
The sums can be used to compute means.
"""

import csv
import cPickle as pickle

class Keyer:
    def __init__(self, cols):
        names = ["security_id", "initiator"]
        self.indices = [cols[name] for name in names]

    def get_key(self, row):
        return tuple(row[index] for index in self.indices)


def _new_item():
    """An item contains:
        num_aggregated_rows
        sum_bid_changes at events 50:100
        sum_ask_changes at events 50:100
    """
    return [0] * 101


def _numerize(row, start, end, step):
    return [float(row[i]) for i in xrange(start, end, step)]


def main():
    data_path = "../data_atrade/training.csv"
    with open(data_path, "rb") as input:
        reader = csv.reader(input, delimiter=",")
        row = reader.next()
        cols = dict((name, i) for i, name in enumerate(row))

        keyer = Keyer(cols)
        changes = dict()
        bid_start = cols["bid51"]
        bid_end = cols["bid100"] + 1
        bid_base_col = cols["bid50"]
        for i, row in enumerate(reader):
            if i % 1000 == 0:
                print i
            key = keyer.get_key(row)
            item = changes.get(key)
            if item is None:
                item = _new_item()
                changes[key] = item


            bids = _numerize(row, bid_start, bid_end, step=2)
            asks = _numerize(row, bid_start + 1, bid_end + 1, step=2)
            bid_base = float(row[bid_base_col])
            ask_base = float(row[bid_base_col + 1])
            item[0] += 1
            for i in xrange(len(bids)):
                item[2 * i + 1] += bids[i] - bid_base
                item[2 * i + 2] += asks[i] - ask_base


    with open("changes.pickle", "wb") as output:
        pickle.dump(changes, output)


if __name__ == "__main__":
    main()
