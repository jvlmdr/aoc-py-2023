'''

'''

import collections
import functools
import itertools
import pprint
import re
import sys

import numpy as np


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]

    grid = np.array([list(s) for s in lines])
    shape = tuple(grid.shape)

    active = np.zeros(grid.shape, dtype=bool)
    visited = set()
    to_visit = collections.deque([((0, 0), (0, 1))])
    while to_visit:
        x, prev = to_visit.popleft()
        active[x] = True
        if (x, prev) in visited:
            continue
        visited.add((x, prev))

        steps = []
        if grid[x] == '.':
            steps.append(prev)
        elif grid[x] == '\\':
            curr = ()
            if prev == (0, 1):
                curr = (1, 0)
            elif prev == (0, -1):
                curr = (-1, 0)
            elif prev == (1, 0):
                curr = (0, 1)
            elif prev == (-1, 0):
                curr = (0, -1)
            steps.append(curr)
        elif grid[x] == '/':
            curr = ()
            if prev == (0, 1):
                curr = (-1, 0)
            elif prev == (0, -1):
                curr = (1, 0)
            elif prev == (1, 0):
                curr = (0, -1)
            elif prev == (-1, 0):
                curr = (0, 1)
            steps.append(curr)
        elif grid[x] == '-':
            if prev == (0, 1) or prev == (0, -1):
                steps.append(prev)
            else:
                steps.append((0, 1))
                steps.append((0, -1))
        elif grid[x] == '|':
            if prev == (1, 0) or prev == (-1, 0):
                steps.append(prev)
            else:
                steps.append((1, 0))
                steps.append((-1, 0))
        else:
            raise ValueError(f'Unknown grid value: {grid[x]}')

        for step in steps:
            new_x = x[0] + step[0], x[1] + step[1]
            if 0 <= new_x[0] < shape[0] and 0 <= new_x[1] < shape[1] and (new_x, step) not in visited:
                to_visit.append((new_x, step))

        # pprint.pprint([''.join(['#' if c else '.' for c in row]) for row in active])
        print('queue size:', len(to_visit))

    print(np.sum(active))


if __name__ == '__main__':
    main()
