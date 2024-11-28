'''
--- Day 13: Point of Incidence ---
With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:

123456789
    ><
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><
123456789
In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7
This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.

Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?
'''

import collections
import functools
import itertools
import re
import sys

import numpy as np


def split_lines(lines):
    curr = []
    for line in lines:
        if not line:
            yield curr
            curr = []
        else:
            curr.append(line)
    if curr:
        yield curr


def to_array(lines):
    num_rows = len(lines)
    num_cols, = set(len(line) for line in lines)
    rows = []
    for line in lines:
        rows.append([c == '#' for c in line])
    return np.asarray(rows)


def count_different(arr, i):
    a = arr[:i][::-1]
    b = arr[i:]
    n = min(len(a), len(b))
    return np.count_nonzero(a[:n] != b[:n])


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]
    patterns = list(map(to_array, split_lines(lines)))

    total = 0
    for index, arr in enumerate(patterns):
        m, n = arr.shape
        for j in range(1, n):
            if count_different(arr.T, j) == 1:
                print(index, 'col', j)
                total += j
        for i in range(1, m):
            if count_different(arr, i) == 1:
                print(index, 'row', i)
                total += 100 * i

    print(total)




if __name__ == '__main__':
    main()
