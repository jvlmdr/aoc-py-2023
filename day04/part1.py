import re
import sys


CARD_RE = re.compile(r'Card +(\d+): (.*) \| (.*)')
SPACE_RE = re.compile(r' +')

def main():
    with open(sys.argv[1]) as f:
        lines = [s.strip() for s in f]

    total = 0
    for line in lines:
        m = CARD_RE.match(line)
        lhs_str = m[2]
        rhs_str = m[3]
        lhs = set([int(s) for s in SPACE_RE.split(lhs_str) if s])
        rhs = [int(s) for s in SPACE_RE.split(rhs_str) if s]
        n = sum(1 for x in rhs if x in lhs)
        if n:
            total += 2 ** (n - 1)
    print(total)

main()

