'''
--- Day 14: Parabolic Reflector Dish ---
You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1
The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?
'''

import collections
import functools
import itertools
import pprint
import re
import sys

import numpy as np


def roll_rocks(column):
    square_positions = [i for i, c in enumerate(column) if c == '#']
    positions = [0] + [i + 1 for i in square_positions]
    segments = column.split('#')
    circle_counts = [sum(c == 'O' for c in seg) for seg in segments]
    return [(i, n) for i, n in zip(positions, circle_counts) if n > 0]


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]

    num_cols = len(lines[0])
    cols = [''.join([line[i] for line in lines]) for i in range(num_cols)]
    rolled_cols = [roll_rocks(col) for col in cols]

    loads = [
        [num_cols - (start + i) for start, count in pairs for i in range(count)]
        for pairs in rolled_cols
    ]
    pprint.pprint(loads)
    print(sum([sum(col) for col in loads]))

    # # Find the cells that are non-blocking.
    # blocking = np.asarray([[c != '#' for c in line] for line in lines])
    # is_free = np.logical_and.accumulate(blocking, axis=0)
    # is_sphere = np.asarray([[c == 'O' for c in line] for line in lines])
    # is_free_sphere = is_sphere & is_free
    # counts = np.sum(is_free_sphere, axis=0)
    # n, _ = blocking.shape
    # # Take sum from south edge.
    # loads = [[n - i for i in range(count)] for count in counts]
    # pprint.pprint(loads)



if __name__ == '__main__':
    main()
