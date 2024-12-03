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


def main():
    with open(sys.argv[1]) as f:
        grid = [s.rstrip('\n') for s in f]
    grid = np.array(list(map(list, grid)))
    nrows, ncols = grid.shape
    start = (0, 1)
    goal = (nrows - 1, ncols - 2)
    # Find edges in the grid.
    edges = collections.defaultdict(dict)
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
                edges[(i, j)][ni, nj] = 1
    edges = dict(edges)

    # Prune trivial vertices.
    print('original:', len(edges))
    for x in list(edges):
        if len(edges[x]) == 2:
            (a, ax), (b, bx) = edges[x].items()
            del edges[a][x]
            del edges[b][x]
            del edges[x]
            edges[a][b] = ax + bx
            edges[b][a] = ax + bx
    print('simplified:', len(edges))

    def dfs(node, visited, path_len):
        if node == goal:
            yield path_len
        visited.add(node)
        for neighbor, edge_dist in edges[node].items():
            if neighbor in visited:
                continue
            yield from dfs(neighbor, visited, path_len + edge_dist)
        visited.remove(node)

    max_path_len = 0
    for x in dfs(start, set(), 0):
        if x > max_path_len:
            print(x, max_path_len)
            max_path_len = x
    print('max:', max_path_len)


if __name__ == '__main__':
    main()
