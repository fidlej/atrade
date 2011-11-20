#!/usr/bin/env python
"""Usage: %prog training.csv
Displays price changes in a few shocks.
The price of the 50th event is the baseline.
"""

import numpy as np
from matplotlib import pyplot
import csv

import optparse

DEFAULTS = {
        "security": 1,
        "numplots": 1000,
        "initiator": "B",
        "price": "ask",
        }

def _parse_args():
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-s", "--security", type="int",
        help="display curves of the given security (default=%(security)s" %
        DEFAULTS)
    parser.add_option("-n", "--numplots", type="int",
        help="set the number of plots (default=%(numplots)s)" % DEFAULTS)
    parser.add_option("-i", "--initiator", choices=["B", "S"],
        help="filter by initiator (default=%(initiator)s)" % DEFAULTS)
    parser.add_option("-p", "--price", choices=["ask", "bid"],
        help="display the given prices (default=%(price)s)" % DEFAULTS)
    parser.set_defaults(**DEFAULTS)

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("one path to training.csv is expected")

    (data_path,) = args
    return options, data_path


def _numerize(row, start, end, step):
    """Converts the given range of string to floats.
    """
    return [float(row[i]) for i in xrange(start, end, step)]


def main():
    options, data_path = _parse_args()
    with open(data_path, "rb") as input:
        reader = csv.reader(input, delimiter=",")
        row = reader.next()
        columns = dict((name, i) for i, name in enumerate(row))

        start_t = 40
        start = columns[options.price + str(start_t)]
        mid_end = columns[options.price + "50"] + 1
        mid_start = columns[options.price + "51"]
        end = columns[options.price + "100"] + 1
        base_col = columns[options.price + "50"]

        i = 0
        while i < options.numplots:
            row = reader.next()
            security_id = int(row[columns["security_id"]])
            if security_id != options.security:
                continue
            initiator = row[columns["initiator"]]
            if initiator != options.initiator:
                continue

            i += 1
            y = np.asarray(
                    _numerize(row, start, mid_end, step=4) +
                    _numerize(row, mid_start, end, step=2))
            y -= float(row[base_col])
            x = xrange(start_t, 100 + 1)
            assert len(x) == len(y)
            pyplot.plot(x, y)
        pyplot.show()


if __name__ == "__main__":
    main()

