

DIGITS = {
    **{str(k): k for k in range(10)},
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}


def find_digits(line):
    out = []
    for i in range(len(line)):
        for k, v in DIGITS.items():
            if line[i:].startswith(k):
                out.append(v)
    return out


def main():
    with open('input.txt') as f:
        lines = list(f)

    for line in lines:
        print(line, find_digits(line))

    print(sum(10 * line[0] + line[-1] for line in map(find_digits, lines)))


if __name__ == '__main__':
    main()
