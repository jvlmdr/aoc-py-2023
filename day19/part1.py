import collections
import functools
import itertools
from pprint import pprint
import re
import sys

import numpy as np
from tqdm import tqdm


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


def evaluate_condition(condition, part):
    if condition is None:
        return True
    key, op, value = re.match(r'(\w)([<>]+)(\d+)', condition).groups()
    value = int(value)
    if op == '>':
        return part[key] > value
    elif op == '<':
        return part[key] < value
    return False


def process_part(workflows, part):
    current_workflow = 'in'
    while True:
        for condition, destination in workflows[current_workflow]:
            if evaluate_condition(condition, part):
                if destination == 'A':
                    return 'A'
                elif destination == 'R':
                    return 'R'
                else:
                    current_workflow = destination
                    break


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]
    workflows, parts = parse_input(lines)

    total_sum = 0
    for part in parts:
        result = process_part(workflows, part)
        if result == 'A':
            total_sum += sum(part.values())
    print(total_sum)


if __name__ == '__main__':
    main()
