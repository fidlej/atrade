#!/usr/bin/env python

import csv
import cPickle as pickle


from means import Keyer


def main():
    data_path = "../data_atrade/testing.csv"

    with open("changes.pickle", "rb") as pickled:
        changes = pickle.load(pickled)

    with open("response.csv", "wb") as output:
        with open(data_path, "rb") as input:
            reader = csv.reader(input, delimiter=",")
            row = reader.next()
            cols = dict((name, i) for i, name in enumerate(row))

            output.write("%s\n" % ",".join(row))

            keyer = Keyer(cols)
            row_id_col = cols["row_id"]
            bid_base_col = cols["bid50"]
            for i, row in enumerate(reader):
                if i % 1000 == 0:
                    print i
                key = keyer.get_key(row)
                item = changes.get(key)
                num_aggregated = item[0]

                bid_base = float(row[bid_base_col])
                ask_base = float(row[bid_base_col + 1])
                bids = []
                asks = []
                for i in xrange(50):
                    bid = item[2 * i + 1] / float(num_aggregated) + bid_base
                    ask = item[2 * i + 2] / float(num_aggregated) + ask_base
                    bids.append(bid)
                    asks.append(ask)

                    if i == 0:
                        # The prices in event50 and even51 are always the same.
                        assert bid == bid_base
                        assert ask == ask_base

                formatted = ",".join("%f,%f" % (bid, ask) for bid, ask in
                        zip(bids, asks))
                output.write("%s,%s\n" % (row[row_id_col], formatted))


main()
