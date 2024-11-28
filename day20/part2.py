import collections
import functools
import itertools
import math
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
        k: 0 if module_type == FLIPFLOP else
            collections.OrderedDict((u, 0) for u in modules['in'][k])
        for k, module_type in modules['type'].items()
        if module_type in {FLIPFLOP, CONJUNCTION}
    }


def simulate(modules, state):
    # Modifies state and rx_counts in place!
    queue = collections.deque()
    queue.append(('button', 'broadcaster', 0))
    counts = [0, 0]
    rx_counts = collections.defaultdict(lambda: [0, 0])
    tx_counts = collections.defaultdict(lambda: [0, 0])

    while queue:
        prev, curr, msg = queue.popleft()
        counts[msg] += 1
        tx_counts[prev][msg] += 1
        rx_counts[curr][msg] += 1
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

    return counts, dict(rx_counts), dict(tx_counts)


def find_ancestors(modules, node):
    visited = set()
    queue = collections.deque()
    queue.append(node)
    while queue:
        curr = queue.popleft()
        visited.add(curr)
        if curr == 'broadcaster':
            continue
        for dest in modules['in'][curr]:
            if dest not in visited:
                queue.append(dest)
    return visited


def export_state(modules, state, node):
    '''Exports the state of a node into a hashable form.'''
    if modules['type'][node] == FLIPFLOP:
        return state[node]
    elif modules['type'][node] == CONJUNCTION:
        # Depends on order not being modified in OrderedDict.
        return tuple(state[node].values())
    else:
        raise ValueError(f'No state: {modules["type"][node]}')


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]

    modules = parse_input(lines)
    state = init_state(modules)

    rx_input, = modules['in']['rx']
    assert modules['type'][rx_input] == CONJUNCTION
    final_nodes = modules['in'][rx_input]
    print(final_nodes)

    # Find subgraphs that affect each node in `final_nodes`.
    node_subset = {}
    for node in final_nodes:
        subgraph = find_ancestors(modules, node)
        substate = subgraph.intersection(set(state.keys()))
        node_subset[node] = sorted(substate)

    state_index = {node: {} for node in final_nodes}
    node_outputs = {node: [0] for node in final_nodes}

    i = 0
    cycles = {}
    while len(cycles) < len(final_nodes):
        for node in final_nodes:
            if node in cycles:
                continue
            node_state = tuple([export_state(modules, state, k) for k in node_subset[node]])
            if node_state in state_index[node]:
                offset = state_index[node][node_state]
                period = i - offset
                cycles[node] = (offset, period)
                print(f'Found cycle for {node}: offset {offset}, period {period}')
            state_index[node][node_state] = i
        _, _, tx_counts = simulate(modules, state)
        for node in final_nodes:
            node_outputs[node].append(tx_counts.get(node, [0, 0])[1])
        i += 1

    # Each of the final nodes is only activated once per cycle.
    print({node: sum(node_outputs[node]) for node in final_nodes})
    # Find where each activation occurs.
    index = {node: node_outputs[node].index(1) for node in final_nodes}
    print(index)

    # In fact, it looks like all the periods align. Just take the LCM.
    print(functools.reduce(math.lcm, [period for _, period in cycles.values()]))


if __name__ == '__main__':
    main()
