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
offset by tilting the lever so all of the rocks will slide north as far as they will go:

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


--- Part Two ---
The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
This process should work if you leave it running long enough, but you're still worried about the north support beams. To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?


'''

import collections
import functools
import itertools
import pprint
import re
import sys

import numpy as np

NUM_CYCLES = 1000000000


def roll1(is_square, is_circle):
    n = len(is_square)
    square_inds, = np.where(is_square)
    segs = np.split(is_circle, square_inds)
    starts = [0, *(square_inds + 1)]
    is_circle = np.zeros(n, dtype=bool)
    for a, seg in zip(starts, segs):
        is_circle[a:a + np.sum(seg)] = True
    return is_circle


def roll(is_square, is_circle):
    return np.asarray([roll1(s, c) for s, c in zip(is_square, is_circle)])


def score(is_circle):
    _, n = is_circle.shape
    return np.sum(np.arange(n, 0, -1) * is_circle).item()


def render(is_square, is_circle):
    rows = [
        ''.join(['O' if c else '#' if s else '.' for s, c in zip(ss, cs)])
        for ss, cs in zip(is_square, is_circle)
    ]
    pprint.pprint(rows)


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]

    is_square = np.asarray([[c == '#' for c in line] for line in lines])
    is_circle = np.asarray([[c == 'O' for c in line] for line in lines])

    is_square = np.rot90(is_square, 1)
    is_circle = np.rot90(is_circle, 1)

    history = [score(is_circle)]
    index = {}
    offset = None
    period = None
    i = 0
    while True:
        for _ in range(4):
            is_circle = roll(is_square, is_circle)
            is_square = np.rot90(is_square, -1)
            is_circle = np.rot90(is_circle, -1)
        i += 1
        s = score(is_circle)
        print(i, s)
        history.append(s)

        key = tuple(map(tuple, is_circle))
        if key in index:
            offset = index[key]
            period = i - offset
            break
        else:
            index[key] = i

    print(f'period {period}, offset {offset}')

    # Identify cycle.
    assert offset is not None and period is not None
    i = offset + (NUM_CYCLES - offset) % period
    print(history[i])


if __name__ == '__main__':
    main()
