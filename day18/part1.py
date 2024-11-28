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


def parse_directions(lines):
    directions = []
    for line in lines:
        direction, distance, _ = line.split()
        directions.append((direction, int(distance)))
    return directions


def create_trench(directions):
    x, y = 0, 0
    trench = [(x, y)]

    for direction, distance in directions:
        for _ in range(distance):
            if direction == 'U':
                y -= 1
            elif direction == 'D':
                y += 1
            elif direction == 'L':
                x -= 1
            elif direction == 'R':
                x += 1
            trench.append((x, y))

    assert trench[0] == trench[-1]
    return trench


def is_point_in_polygon(point, polygon):
    x, y = point
    winding_number = 0

    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]

        if y1 <= y:
            if y2 > y and (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1) > 0:
                winding_number += 1
        else:
            if y2 <= y and (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1) < 0:
                winding_number -= 1

    return winding_number != 0


def fill_interior(trench):
    min_x = min(x for x, y in trench)
    max_x = max(x for x, y in trench)
    min_y = min(y for x, y in trench)
    max_y = max(y for x, y in trench)

    filled_trench = set(trench)

    for x in tqdm(range(min_x, max_x + 1)):
        for y in range(min_y, max_y + 1):
            if is_point_in_polygon((x, y), trench):
                filled_trench.add((x, y))

    return filled_trench


def calculate_volume(filled_trench):
    return len(filled_trench)


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]

    directions = parse_directions(lines)
    trench = create_trench(directions)
    filled_trench = fill_interior(trench)
    volume = calculate_volume(filled_trench)

    print(volume)


if __name__ == '__main__':
    main()
