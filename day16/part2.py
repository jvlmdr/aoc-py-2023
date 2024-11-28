r'''
--- Day 16: The Floor Will Be Lava ---
With the beam of light completely focused somewhere, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

If the beam encounters empty space (.), it continues in the same direction.
If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..
Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?


--- Part Two ---
As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel. There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner; for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava, you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..
Using this configuration, 51 tiles are energized:

.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..
Find the initial beam configuration that energizes the largest number of tiles; how many tiles are energized in that configuration?
'''

import collections
import functools
import itertools
from pprint import pprint
import re
import sys

import numpy as np
from tqdm import tqdm


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]

    grid = np.array([list(s) for s in lines])
    nrows, ncols = grid.shape

    # Find the maximum number of energized tiles.
    starts = (
        [((i, 0), (0, 1)) for i in range(nrows)] +
        [((i, ncols - 1), (0, -1)) for i in range(nrows)] +
        [((0, i), (1, 0)) for i in range(ncols)] +
        [((nrows - 1, i), (-1, 0)) for i in range(ncols)]
    )
    print(max(count_active(grid, start, start_dir) for start, start_dir in tqdm(starts)))


def count_active(grid, start, start_dir):
    shape = tuple(grid.shape)
    active = np.zeros(grid.shape, dtype=bool)
    visited = set()
    to_visit = collections.deque([(start, start_dir)])
    while to_visit:
        x, prev = to_visit.popleft()
        active[x] = True
        if (x, prev) in visited:
            continue
        visited.add((x, prev))

        steps = []
        if grid[x] == '.':
            steps.append(prev)
        elif grid[x] == '\\':
            curr = ()
            if prev == (0, 1):
                curr = (1, 0)
            elif prev == (0, -1):
                curr = (-1, 0)
            elif prev == (1, 0):
                curr = (0, 1)
            elif prev == (-1, 0):
                curr = (0, -1)
            steps.append(curr)
        elif grid[x] == '/':
            curr = ()
            if prev == (0, 1):
                curr = (-1, 0)
            elif prev == (0, -1):
                curr = (1, 0)
            elif prev == (1, 0):
                curr = (0, -1)
            elif prev == (-1, 0):
                curr = (0, 1)
            steps.append(curr)
        elif grid[x] == '-':
            if prev == (0, 1) or prev == (0, -1):
                steps.append(prev)
            else:
                steps.append((0, 1))
                steps.append((0, -1))
        elif grid[x] == '|':
            if prev == (1, 0) or prev == (-1, 0):
                steps.append(prev)
            else:
                steps.append((1, 0))
                steps.append((-1, 0))
        else:
            raise ValueError(f'Unknown grid value: {grid[x]}')

        for step in steps:
            new_x = x[0] + step[0], x[1] + step[1]
            if 0 <= new_x[0] < shape[0] and 0 <= new_x[1] < shape[1] and (new_x, step) not in visited:
                to_visit.append((new_x, step))

    return np.sum(active)


if __name__ == '__main__':
    main()
