import numpy as np


def find_numbers(value):
    out = []
    start = None
    curr = 0
    for i, x in enumerate(value):
        if x >= 0:
            if start is None:
                start = i
                curr = x
            else:
                curr = curr * 10 + x
        else:
            if start is not None:
                out.append((start, i, curr))
            start = None
    if start is not None:
        out.append((start, len(value), curr))
    return out


def main():
    with open('input.txt') as f:
        lines = [s.strip() for s in f.readlines()]

    is_dot = np.asarray([[c == '.' for c in l] for l in lines])
    value = np.asarray([
        [int(c) if '0' <= c and c <= '9' else -1 for c in l]
        for l in lines])
    is_number = value >= 0
    is_part = ~is_dot & ~is_number
    is_adjacent = np.zeros_like(is_part)
    is_adjacent |= is_part
    is_adjacent[1:, :] |= is_part[:-1, :]
    is_adjacent[1:, 1:] |= is_part[:-1, :-1]
    is_adjacent[:, 1:] |= is_part[:, :-1]
    is_adjacent[:-1, 1:] |= is_part[1:, :-1]
    is_adjacent[:-1, :] |= is_part[1:, :]
    is_adjacent[:-1, :-1] |= is_part[1:, 1:]
    is_adjacent[:, :-1] |= is_part[:, 1:]
    is_adjacent[1:, :-1] |= is_part[:-1, 1:]

    total = 0
    for line, line_value, line_adjacent in zip(lines, value, is_adjacent):
        print(''.join('X' if x else ' ' for x in line_adjacent))
        # print(''.join(str(x) if x >= 0 else ' ' for x in line_value))
        # print([n for a, b, n in find_numbers(line_value) if np.any(line_adjacent[a:b])])
        total += sum(
            n for a, b, n in find_numbers(line_value)
            if np.any(line_adjacent[a:b]))
    print(total)

main()
