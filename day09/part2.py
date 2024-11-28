import sys

import numpy as np


def extrapolate(line):
    if np.all(line == 0):
        return np.zeros(len(line) + 1, dtype=int)
    start = line[0]
    delta = np.diff(line)
    delta = extrapolate(delta)
    line = np.cumsum(np.concatenate([[0], delta]))
    line = line - line[1] + start
    return line


def main():
    with open(sys.argv[1]) as f:
        rows = [np.asarray(list(map(int, s.strip().split())), int) for s in f]

    rows = list(map(extrapolate, rows))
    print(sum(row[0] for row in rows))


main()
