import collections
import functools
import itertools
from pprint import pprint
import re
import sys

import numpy as np
from tqdm import tqdm

BROADCASTER = 'broadcaster'
FLIPFLOP = 'flipflop'
CONJUNCTION = 'conjunction'


def parse_input(lines):
    module_order = []
    module_types = {}
    out_edges = {}
    in_edges = collections.defaultdict(list)
    for line in lines:
        parts = line.split(' -> ')
        name = parts[0]
        destinations = parts[1].split(', ')
        if name == 'broadcaster':
            module_name, module_type = name, BROADCASTER
        elif name.startswith('%'):
            module_name, module_type = name[1:], FLIPFLOP
        elif name.startswith('&'):
            module_name, module_type = name[1:], CONJUNCTION
        else:
            raise ValueError(f'Unknown module type: {name}')
        module_order.append(module_name)
        module_types[module_name] = module_type
        out_edges[module_name] = destinations
        for dest in destinations:
            in_edges[dest].append(module_name)
    in_edges = dict(in_edges)
    return {'type': module_types, 'out': out_edges, 'in': in_edges, 'order': module_order}


def init_state(modules):
    return {
        k: 0 if module_type == FLIPFLOP else {u: 0 for u in modules['in'][k]}
        for k, module_type in modules['type'].items()
        if module_type in {FLIPFLOP, CONJUNCTION}
    }


def simulate(modules, state):
    queue = collections.deque()
    queue.append(('button', 'broadcaster', 0))
    counts = [0, 0]

    while queue:
        prev, curr, msg = queue.popleft()
        counts[msg] += 1
        if curr not in modules['type']:
            # Endpoint; ignore.
            continue
        if modules['type'][curr] == FLIPFLOP:
            if not msg:
                state[curr] = int(not state[curr])
                for dest in modules['out'][curr]:
                    queue.append((curr, dest, state[curr]))
        elif modules['type'][curr] == CONJUNCTION:
            state[curr][prev] = msg
            output = int(not all(state[curr].values()))
            for dest in modules['out'][curr]:
                queue.append((curr, dest, output))
        elif modules['type'][curr] == BROADCASTER:
            for dest in modules['out'][curr]:
                queue.append((curr, dest, msg))
        else:
            raise ValueError(f'Unknown module type: {modules["type"][curr]}')

    return counts


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]

    modules = parse_input(lines)
    state = init_state(modules)
    totals = np.zeros(2, dtype=int)
    for i in range(1000):
        counts = simulate(modules, state)
        print(counts)
        totals += np.asarray(counts)
    print(totals)
    print(np.prod(totals))


if __name__ == '__main__':
    main()
