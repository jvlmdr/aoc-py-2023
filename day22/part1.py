import collections
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


def find_safe_to_disintegrate(settled):
    # Find which bricks are supporting other bricks.
    # Then find bricks where all bricks that they support are supported by others.
    supports = settled['supports']
    supported_by = settled['supported_by']
    safe = []
    for i in range(len(settled['bricks'])):
        if all(len(supported_by.get(j, [])) > 1 for j in supports.get(i, [])):
            safe.append(i)

    return safe


def main():
    if len(sys.argv) < 2:
        print("Please provide input file")
        return

    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()

    bricks = parse_bricks(lines)
    min_x = min(brick[0][0] for brick in bricks)
    min_y = min(brick[0][1] for brick in bricks)
    max_x = max(brick[1][0] for brick in bricks)
    max_y = max(brick[1][1] for brick in bricks)
    print(f'({min_x},{min_y})-({max_x},{max_y})')

    settled = settle_bricks(bricks)
    print('max z1:', max(b[0][2] for b in settled['bricks']))
    safe_bricks = find_safe_to_disintegrate(settled)
    pprint(dict(collections.Counter([len(s_i) for s_i in settled['supports'].values()])))
    print(len(safe_bricks))


if __name__ == "__main__":
    main()