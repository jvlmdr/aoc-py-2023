import collections
import heapq
import math
from pprint import pprint
import sys

import numpy as np


def parse_bricks(lines):
    bricks = []
    for line in lines:
        start, end = line.strip().split('~')
        start = tuple(map(int, start.split(',')))
        end = tuple(map(int, end.split(',')))
        assert all(a <= b for a, b in zip(start, end))
        bricks.append((start, end))
    return bricks


def intersect(x, y):
    xa, xb = x
    ya, yb = y
    return tuple(map(max, xa, ya)), tuple(map(min, xb, yb))


def volume(interval):
    return math.prod(max(0, b - a + 1) for a, b in zip(*interval))


def settle_bricks(bricks):
    settled = []
    # Sort by lower z coordinate.
    bricks = sorted(bricks, key=lambda x: x[0][2])
    supported_by = {}

    for i, (brick_a, brick_b) in enumerate(bricks):
        below = [
            (j, (other_a, other_b)) for j, (other_a, other_b) in enumerate(settled)
            if volume(intersect((other_a[:2], other_b[:2]), (brick_a[:2], brick_b[:2])))
        ]
        max_z = max([z_b for _, (_, (_, _, z_b)) in below], default=0)
        supported_by[i] = [j for j, (_, (_, _, z_b)) in below if z_b == max_z]
        new_z = max_z + 1
        settled_a = brick_a[:2] + (new_z,)
        settled_b = brick_b[:2] + (new_z + brick_b[2] - brick_a[2],)
        settled.append((settled_a, settled_b))

    supports = collections.defaultdict(list)
    for i, s in supported_by.items():
        for j in s:
            supports[j].append(i)
    supports = {k: sorted(v) for k, v in supports.items()}

    return {
        'bricks': settled,
        'supported_by': supported_by,
        'supports': supports,
    }


def count_chain_reaction(settled):
    # The set of bricks which will fall if brick `i` is removed is the union of
    # - bricks that are supported by brick `i`
    # - bricks that will fall if we remove each of these
    # - bricks that will fall only if we remove multiple bricks
    # Nevertheless, this could reduce the amount of computation.
    # Furthermore, there must be a past through the brick graph to these bricks.

    # Implement naive solution to start with.

    bricks = settled['bricks']
    supports = settled['supports']
    supported_by = settled['supported_by']
    n = len(bricks)
    count = [0 for _ in range(n)]

    for i, (brick_a, brick_b) in enumerate(bricks):
        # Prioritize by brick index in supported structure.
        # This is a topological ordering of the support graph.
        queue = supports.get(i, [])
        heapq.heapify(queue)
        gone = {i}
        while queue:
            j = heapq.heappop(queue)
            if j in gone:
                continue
            # Check whether this brick will fall (yet).
            if all(k in gone for k in supported_by.get(j, [])):
                gone.add(j)
                for k in supports.get(j, []):
                    heapq.heappush(queue, k)
        count[i] = len(gone) - 1

    return count


def main():
    if len(sys.argv) < 2:
        print("Please provide input file")
        return

    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()

    bricks = parse_bricks(lines)
    settled = settle_bricks(bricks)

    counts = count_chain_reaction(settled)
    print(counts)
    print(sum(counts))


if __name__ == "__main__":
    main()