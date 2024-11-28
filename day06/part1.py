import sys
import re

import numpy as np


def main():
    with open(sys.argv[1]) as f:
        lines = [re.split(r' +', s.strip()) for s in f]
    times = [int(s) for s in lines[0][1:]]
    dists = [int(s) for s in lines[1][1:]]

    n_ways = [
        sum(1 for x in range(t + 1) if (t - x) * x > d)
        for t, d in zip(times, dists)
    ]
    print(n_ways)
    print(np.prod(n_ways))


main()
