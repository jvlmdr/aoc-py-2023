import sys
import re

import numpy as np


def main():
    with open(sys.argv[1]) as f:
        lines = [re.split(r' +', s.strip()) for s in f]
    times = [int(s) for s in lines[0][1:]]
    dists = [int(s) for s in lines[1][1:]]

    t = int(''.join(map(str, times)))
    d = int(''.join(map(str, dists)))

    a = -1
    b = t
    c = -d
    delta2 = float(b) ** 2 - 4 * a * c
    half = np.sqrt(delta2) / np.abs(2 * a)
    center = -b / (2 * a)

    u = int(np.ceil(center - half))
    v = int(np.floor(center + half))
    print(u, v)
    print(v - u + 1)


main()
