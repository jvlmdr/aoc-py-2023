import itertools
import pprint
import re
import sys


def parse(lines):
    init_seeds = [int(s) for s in lines[0].split()[1:]]
    lines = lines[1:]
    curr_map = []
    maps = []
    for line in lines:
        if not line:
            continue
        elif re.match('[a-z]+-to-[a-z]+ map:', line):
            if curr_map:
                maps.append(sorted(curr_map))
            curr_map = []
        else:
            start_y, start_x, n = (int(s) for s in line.split(' '))
            curr_map.append((start_y, start_x, n))
    if curr_map:
        maps.append(sorted(curr_map))
    return init_seeds, maps


def range_map_apply(range_map, x):
    ys = [
        start_y + (x - start_x) for start_y, start_x, n in range_map
        if start_x <= x and x < start_x + n
    ]
    if len(ys) > 1:
        raise ValueError('multiple matches')
    try:
        y, = ys
        return y
    except ValueError:
        return x


def range_map_apply_interval(range_map, interval):
    # Divide interval into segments.
    a, n = interval
    start_xs = [start_x for _, start_x, _ in range_map]
    stop_xs = [start_x + n for _, start_x, n in range_map]
    knot_xs = sorted(set([a, a + n, *start_xs, *stop_xs]))
    knot_xs = [x for x in knot_xs if a <= x and x <= a + n]
    knot_intervals = [
        (start_x, stop_x - start_x)
        for start_x, stop_x in zip(knot_xs, knot_xs[1:])
    ]
    return [
        (range_map_apply(range_map, start_x), n)
        for start_x, n in knot_intervals
    ]


def main():
    with open(sys.argv[1]) as f:
        lines = [s.strip() for s in f]

    seeds, range_maps = parse(lines)
    seed_intervals = list(zip(seeds[::2], seeds[1::2]))
    for m in range_maps:
        seed_intervals = sorted(itertools.chain.from_iterable(
            range_map_apply_interval(m, xn) for xn in seed_intervals))
        print(len(seed_intervals))
    print(min(seed_intervals))


main()
