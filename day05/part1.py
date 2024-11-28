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


def main():
    with open(sys.argv[1]) as f:
        lines = [s.strip() for s in f]

    seeds, range_maps = parse(lines)
    print(seeds)
    for m in range_maps:
        seeds = [range_map_apply(m, x) for x in seeds]
        print(seeds)
    print(min(seeds))


main()
