import collections
import functools
import itertools
from pprint import pprint
import re
import sys

import numpy as np
from tqdm import tqdm

CONDITION_PATTERN = re.compile(r'(\w)([<>])(\d+)')
Part = collections.namedtuple('Part', ['x', 'm', 'a', 's'])
MAX_VALUE = 4000


def parse_input(lines):
    n, = [i for i, line in enumerate(lines) if not line]
    workflow_lines = lines[:n]
    parts_lines = lines[n+1:]

    workflows = {}
    for line in workflow_lines:
        name, rules_str = line.split('{')
        name = name.strip()
        rules_str = rules_str.rstrip('}')
        rules = []
        for rule in rules_str.split(','):
            if ':' in rule:
                condition, destination = rule.split(':')
                rules.append((condition.strip(), destination.strip()))
            else:
                rules.append((None, rule.strip()))
        workflows[name] = rules

    parts = []
    for line in parts_lines:
        part = {}
        for item in line.strip('{}').split(','):
            key, value = item.split('=')
            part[key.strip()] = int(value.strip())
        parts.append(part)

    return workflows, parts


def parse_condition(s):
    m = CONDITION_PATTERN.match(s)
    field, op, threshold = m.groups()
    return field, op, int(threshold)


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]
    workflows, _ = parse_input(lines)

    init_state = ('in', Part((1, MAX_VALUE), (1, MAX_VALUE), (1, MAX_VALUE), (1, MAX_VALUE)))
    queue = [init_state]
    accepted = []
    while queue:
        key, part_interval = queue.pop()
        if key == 'A':
            accepted.append(part_interval)
            continue
        if key == 'R':
            continue
        rules = workflows[key]
        for condition, destination in rules:
            if condition is None:
                queue.append((destination, part_interval))
            else:
                field, op, threshold = parse_condition(condition)
                curr_interval = getattr(part_interval, field)
                if op == '<':
                    pass_interval = (1, threshold - 1)
                    fail_interval = (threshold, MAX_VALUE)
                elif op == '>':
                    pass_interval = (threshold + 1, MAX_VALUE)
                    fail_interval = (1, threshold)
                pass_interval = (max(pass_interval[0], curr_interval[0]), min(pass_interval[1], curr_interval[1]))
                fail_interval = (max(fail_interval[0], curr_interval[0]), min(fail_interval[1], curr_interval[1]))
                if pass_interval[0] <= pass_interval[1]:
                    queue.append((destination, part_interval._replace(**{field: pass_interval})))
                if fail_interval[0] <= fail_interval[1]:
                    # Update the current interval to the fail interval.
                    part_interval = part_interval._replace(**{field: fail_interval})
                else:
                    # Range is empty. Do not read more rules.
                    break

    total = 0
    for part_interval in accepted:
        interval_lens = [max(0, y - x + 1) for x, y in part_interval]
        print(interval_lens)
        total += functools.reduce(lambda x, y: x * y, interval_lens, 1)
    print(total)


if __name__ == '__main__':
    main()
