import itertools
import re
import sys


NODE_RE = re.compile(r'([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)$')
DIRECTION_KEY = {'L': 0, 'R': 1}


def parse_nodes(lines):
    nodes = {}
    for line in lines:
        m = NODE_RE.match(line)
        nodes[m[1]] = (m[2], m[3])
    return nodes


def main():
    with open(sys.argv[1]) as f:
        lines = [s.strip() for s in f]

    directions = lines[0]
    nodes = parse_nodes(lines[2:])

    curr = 'AAA'
    n = 0
    for direction in itertools.cycle(directions):
        print(curr)
        if curr == 'ZZZ':
            break
        curr = nodes[curr][DIRECTION_KEY[direction]]
        n += 1

    print(n)


main()
