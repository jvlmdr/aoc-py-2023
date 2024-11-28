r'''

'''

import collections
import functools
import itertools
from pprint import pprint
import re
import sys

import numpy as np
from tqdm import tqdm


HEX_PATTERN = re.compile(r'\(\#([0-9a-f]+)\)')


def parse_directions(lines):
    directions = []
    for line in lines:
        hex_code = line.split()[2]  # Extract the hexadecimal code
        hex_code = HEX_PATTERN.match(hex_code).group(1)
        distance = int(hex_code[:5], 16)  # First five digits as distance
        direction_code = hex_code[5]  # Last digit as direction
        direction = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}[direction_code]
        directions.append((direction, distance))
    return directions


def create_trench(directions):
    x, y = 0, 0
    trench = [(x, y)]

    for direction, distance in directions:
        if direction == 'U':
            y -= distance
        elif direction == 'D':
            y += distance
        elif direction == 'L':
            x -= distance
        elif direction == 'R':
            x += distance
        trench.append((x, y))

    return trench


def calculate_volume(trench):
    assert trench[0] == trench[-1]
    unique_xs = sorted(set(x for x, y in trench))

    # Consider intervals [x, x] and (x1, x2).
    intervals = sorted(set(
        [(x, x+1) for x in unique_xs] +
        [(x1 + 1, x2) for x1, x2 in zip(unique_xs, unique_xs[1:]) if x1 + 1 < x2]
    ))
    print('intervals', intervals)

    # Measure the interior volume in [xa, xb).
    interior_vol = 0
    for xa, xb in intervals:
        edges = []
        for (prev_x, prev_y), (curr_x, curr_y) in zip(trench, trench[1:]):
            if prev_y != curr_y:
                continue
            # Count signed crossings of xa.
            if prev_x < xa <= curr_x:
                edges.append((curr_y, 1))
            if curr_x < xa <= prev_x:
                edges.append((curr_y, -1))
            # Count signed crossings of xb.
            if prev_x < xb <= curr_x:
                edges.append((curr_y, 1))
            if curr_x < xb <= prev_x:
                edges.append((curr_y, -1))
        edges = sorted(edges)
        # Walk along crossings and accumulate signed crossings.
        num = {}
        curr = 0
        for y, sign in edges:
            curr += sign
            num[y] = curr
        num = sorted(num.items())
        seg_vol = 0
        for (ya, na), (yb, _) in zip(num, num[1:]):
            assert na >= 0
            if na == 2:
                seg_vol += (xb - xa) * (yb - ya - 1)
        # print((xa, xb), num, seg_vol)
        interior_vol += seg_vol
    print('interior_vol', interior_vol)

    perim = sum(
        abs(prev_x - curr_x) + abs(prev_y - curr_y)
        for (prev_x, prev_y), (curr_x, curr_y) in zip(trench, trench[1:])
    )
    print('perim', perim)

    return interior_vol + perim


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]

    directions = parse_directions(lines)
    trench = create_trench(directions)
    volume = calculate_volume(trench)

    print(volume)


if __name__ == '__main__':
    main()
