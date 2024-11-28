import re
import sys


CARD_RE = re.compile(r'Card +(\d+): (.*) \| (.*)')
SPACE_RE = re.compile(r' +')


def process_card(line):
    m = CARD_RE.match(line)
    lhs_str = m[2]
    rhs_str = m[3]
    lhs = set([int(s) for s in SPACE_RE.split(lhs_str) if s])
    rhs = [int(s) for s in SPACE_RE.split(rhs_str) if s]
    return sum(1 for x in rhs if x in lhs)

def main():
    with open(sys.argv[1]) as f:
        lines = [s.strip() for s in f]

    num_matches = [process_card(line) for line in lines]
    num_copies = [1 for _ in num_matches]
    num_rows = len(num_matches)
    for i in range(num_rows):
        print(num_copies[i])
        for j in range(i + 1, min(i + num_matches[i] + 1, num_rows)):
            num_copies[j] += num_copies[i]

    print(sum(num_copies))

main()

