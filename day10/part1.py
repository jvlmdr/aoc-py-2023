import pprint
import sys

import numpy as np


CONNECTIONS = {
    'S': {(1, 0), (0, 1), (-1, 0), (0, -1)},
    '-': {(0, 1), (0, -1)},
    '|': {(1, 0), (-1, 0)},
    'F': {(1, 0), (0, 1)},
    '7': {(1, 0), (0, -1)},
    'J': {(-1, 0), (0, -1)},
    'L': {(-1, 0), (0, 1)},
}
CONNECTIONS = {
    ord(k): v for k, v in CONNECTIONS.items()
}


def main():
    with open(sys.argv[1]) as f:
        grid = np.asarray([list(map(ord, s.strip())) for s in f], dtype=int)
    rows, cols = grid.shape

    # Find mutual edges.
    edges = {}
    for i in range(rows):
        for j in range(cols):
            deltas = CONNECTIONS.get(grid[i, j], [])
            edges[i, j] = {(i + delta[0], j + delta[1]) for delta in deltas}

    mutual_edges = {}
    for node, neighbors in edges.items():
        mutual_edges[node] = {
            other for other in neighbors
            if other in edges and node in edges[other]
        }

    (start_i,), (start_j,) = np.where(grid == ord('S'))
    start = (int(start_i), int(start_j))
    prev = list(mutual_edges[start])[0]
    curr = start

    n = 0
    while not (n and curr == start):
        candidates, prev = mutual_edges[curr] - {prev}, curr
        # There should be only a single other node.
        curr, = candidates
        n += 1
    print((n + 1) // 2)


main()
