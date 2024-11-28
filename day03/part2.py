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


def find_numbers_grid(values):
    numbers = {}
    out = []
    i = 1
    for value_line in values:
        out_line = np.zeros(len(value_line), dtype=int)
        for a, b, n in find_numbers(value_line):
            numbers[i] = n
            out_line[a:b] = i
            i += 1
        out.append(out_line)
    return np.asarray(out), numbers


def main():
    with open('input.txt') as f:
        lines = [s.strip() for s in f.readlines()]

    value = np.asarray([
        [int(c) if '0' <= c and c <= '9' else -1 for c in l]
        for l in lines])
    number, number_value = find_numbers_grid(value)

    print(number)

    is_gear = np.asarray([[c == '*' for c in l] for l in lines])
    gear_i, gear_j = np.where(is_gear)
    len_i, len_j = value.shape
    total = 0
    for i, j in zip(gear_i, gear_j):
        number_ids = set(number[
            max(0, i-1):min(len_i, i+2),
            max(0, j-1):min(len_j, j+2)].ravel()) - {0}
        if len(number_ids) == 2:
            print([number_value[x] for x in number_ids])
            total += np.prod([number_value[x] for x in number_ids])

    print(total)

main()
