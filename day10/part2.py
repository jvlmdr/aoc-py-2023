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

    path = []
    while not (path and curr == start):
        path.append(curr)
        candidates, prev = mutual_edges[curr] - {prev}, curr
        # There should be only a single other node.
        curr, = candidates

    # path = np.asarray(path)
    # pos_front = path
    # neg_front = path[::-1]
    # delta = np.diff(path[np.arange(len(path) + 1) % len(path)], axis=0)

    # Look for crossings.
    # Could be made more efficient?
    number = np.zeros((rows - 1, cols), dtype=int)
    for prev, curr in zip([path[-1], *path], path):
        # Column is constant (vertical step).
        if prev[1] == curr[1]:
            j = curr[1]
            if prev[0] < curr[0]:
                number[prev[0], j] = 1
            elif curr[0] < prev[0]:
                number[curr[0], j] = -1

    on_path = np.zeros(grid.shape, dtype=bool)
    for x in path:
        on_path[x] = True
    for on_path_i, grid_i in zip(on_path, grid):
        print(''.join(chr(g) if p else ' ' for p, g in zip(on_path_i, grid_i)))

    for i in range(rows - 1):
        print(''.join('+' if x > 0 else '-' if x < 0 else ' ' for x in number[i]))

    cumsum = np.cumsum(number, axis=1)
    interior = ~on_path[1:, :] & (cumsum != 0)
    exterior = ~on_path[1:, :] & (cumsum == 0)

    for i in range(rows - 1):
        print(''.join('I' if x else ' ' for x in interior[i]))

    print(np.sum(interior))


main()
