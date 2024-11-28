import itertools
import re
import sys
import math
import functools


NODE_RE = re.compile(r'([\w]+) = \(([\w]+), ([\w]+)\)$')
DIRECTION_KEY = {'L': 0, 'R': 1}


def parse_nodes(lines):
    nodes = {}
    for line in lines:
        m = NODE_RE.match(line)
        nodes[m[1]] = (m[2], m[3])
    return nodes


def characterize_cycle(directions, nodes, curr):
    index = {}
    n = 0
    goals = []
    for i, direction in itertools.cycle(enumerate(directions)):
        start = index.get((curr, i))
        if start is not None:
            period = n - start
            goals = [x - start for x in goals if x >= start]
            return start, period, goals

        index[curr, i] = n
        if curr.endswith('Z'):
            goals.append(n)

        curr = nodes[curr][DIRECTION_KEY[direction]]
        n += 1


def main():
    with open(sys.argv[1]) as f:
        lines = [s.strip() for s in f]

    directions = lines[0]
    nodes = parse_nodes(lines[2:])

    init_nodes = [x for x in nodes if x.endswith('A')]
    # Each path must enter a cycle within 270 * 746 < 1e6 steps.
    cycles = [characterize_cycle(directions, nodes, x) for x in init_nodes]

    print(cycles)
    # Assume only one goal within each cycle (observed in input.txt).
    assert all(len(goals) == 1 for _, _, goals in cycles)
    cycles = [(start, period, goals[0]) for start, period, goals in cycles]

    # Treat path leading into cycle as within cycle.
    # (x - start[i]) % period[i] = goal[i]
    # x % period[i] = goal[i] + start[i]
    cycles = [(period, (goal + start) % period) for start, period, goal in cycles]

    print(cycles)
    # Assume that goal occurs at position 0 in cycle (observed in input.txt).
    assert all(goal == 0 for _, goal in cycles)

    # Take LCM of all periods.
    print(functools.reduce(math.lcm, [period for period, _ in cycles]))


main()
