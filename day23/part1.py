import collections
import functools
import heapq
import itertools
import math
from pprint import pprint
import re
import sys

import numpy as np
from tqdm import tqdm

CONN = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DELTA_TO_SLOPE = {
    (0, 1): '>',
    (1, 0): 'v',
    (0, -1): '<',
    (-1, 0): '^',
}
SLOPE_TO_DELTA = {v: k for k, v in DELTA_TO_SLOPE.items()}


def main():
    with open(sys.argv[1]) as f:
        grid = [s.rstrip('\n') for s in f]
    grid = np.array(list(map(list, grid)))
    nrows, ncols = grid.shape
    start = (0, 1)
    goal = (nrows - 1, ncols - 2)
    # Find edges in the grid.
    edges = collections.defaultdict(set)
    for i in range(nrows):
        for j in range(ncols):
            for di, dj in CONN:
                ni, nj = i + di, j + dj
                if grid[i, j] == '#':
                    continue
                if not (0 <= ni < nrows and 0 <= nj < ncols):
                    continue
                if grid[ni, nj] == '#':
                    continue
                if grid[i, j] == '.':
                    if grid[ni, nj] == '.':
                        edges[(i, j)].add((ni, nj))
                    else:
                        slope_di, slope_dj = SLOPE_TO_DELTA[grid[ni, nj]]
                        if (slope_di, slope_dj) == (di, dj):
                            edges[(i, j)].add((ni, nj))
                else:
                    slope_di, slope_dj = SLOPE_TO_DELTA[grid[i, j]]
                    if (slope_di, slope_dj) == (di, dj):
                        edges[(i, j)].add((ni, nj))
    edges = dict(edges)
    edges[goal] = set()

    path_lens = []
    queue = collections.deque()
    queue.append((start, frozenset()))
    while queue:
        node, visited = queue.pop()
        if node == goal:
            print(len(visited))
            path_lens.append(len(visited))
            continue
        visited = visited | {node}
        for neighbor in edges[node]:
            if neighbor in visited:
                continue
            queue.append((neighbor, visited))

    print('max:', max(path_lens))


if __name__ == '__main__':
    main()
