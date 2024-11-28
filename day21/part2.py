import collections
from pprint import pprint
import sys

import numpy as np

DIRECTIONS = np.array([[0, 1], [1, 0], [0, -1], [-1, 0]])

# 26501365 = 202300 * 131 + 65
NUM_PERIODS = 202300


def render_grid(space, occupied):
    m, n = space.shape
    return [
        ''.join([
            'O' if occupied[i, j] else '.' if space[i, j] else '#'
            for j in range(n)
        ]) for i in range(m)
    ]


def main():
    with open(sys.argv[1], 'r') as file:
        lines = [line.strip() for line in file]
    input_map = np.array([list(line) for line in lines])
    start = np.squeeze(np.where(input_map == 'S'))
    space = input_map != '#'

    SAMPLE_PERIODS = 5
    space = np.tile(space, [SAMPLE_PERIODS * 2 + 1, SAMPLE_PERIODS * 2 + 1])
    offset = SAMPLE_PERIODS * 131
    start += offset

    present = np.zeros_like(space)
    present[start[0], start[1]] = True
    pprint(render_grid(
        space[offset:offset+131, offset:offset+131],
        present[offset:offset+131, offset:offset+131]))

    for n in range(131 * SAMPLE_PERIODS + 65):
        if (n - 65) % 131 == 0:
            counts = np.asarray([[
                    np.sum(present[i*131:(i+1)*131, j*131:(j+1)*131])
                    for j in range(2 * SAMPLE_PERIODS + 1)
                ] for i in range(2 * SAMPLE_PERIODS + 1)
            ])
            print(counts)

        inds = np.asarray(np.where(present)).T
        inds = inds[:, None, :] + DIRECTIONS[None, :, :]
        inds = np.reshape(inds, (-1, 2))
        present = np.zeros_like(space)
        present[inds[:, 0], inds[:, 1]] = True
        present = present & space

    counts = np.asarray([
        [np.sum(present[i*131:(i+1)*131, j*131:(j+1)*131])
         for j in range(2 * SAMPLE_PERIODS + 1)]
        for i in range(2 * SAMPLE_PERIODS + 1)])
    print(counts)
    counts = collections.Counter(counts.ravel().tolist())
    print(counts)
    inv_counts = collections.defaultdict(lambda: 0)
    for k, v in counts.items():
        if k > 0:
            inv_counts[v] += k
    print(inv_counts)
    print(
        inv_counts[1] +
        NUM_PERIODS * inv_counts[SAMPLE_PERIODS] +
        (NUM_PERIODS - 1) * inv_counts[SAMPLE_PERIODS - 1] +
        NUM_PERIODS ** 2 * inv_counts[SAMPLE_PERIODS ** 2] +
        (NUM_PERIODS - 1) ** 2 * inv_counts[(SAMPLE_PERIODS - 1) ** 2])


if __name__ == "__main__":
    main()