import collections
import sys


HIGH_CARD = 1
ONE_PAIR = 2
TWO_PAIR = 3
THREE_KIND = 4
FULL_HOUSE = 5
FOUR_KIND = 6
FIVE_KIND = 7

VALUE = {
    'J': 1,
    **{str(n): n for n in range(2, 10)},
    'T': 10,
    'Q': 12,
    'K': 13,
    'A': 14,
}


def parse_line(s):
    s = s.strip()
    cards, bid = s.split(' ')
    return cards, int(bid)


def categorize(cards):
    counts = collections.Counter(cards)
    num_wild = counts['J']
    counts = tuple(sorted([v for k, v in counts.items() if k != 'J' and v > 0]))
    if counts:
        counts = (*counts[:-1], counts[-1] + num_wild)
    else:
        counts = (num_wild,)
    if counts == (5,):
        return FIVE_KIND
    elif counts == (1, 4):
        return FOUR_KIND
    elif counts == (2, 3):
        return FULL_HOUSE
    elif counts == (1, 1, 3):
        return THREE_KIND
    elif counts == (1, 2, 2):
        return TWO_PAIR
    elif counts == (1, 1, 1, 2):
        return ONE_PAIR
    elif counts == (1, 1, 1, 1, 1):
        return HIGH_CARD
    else:
        raise ValueError('should not occur')


def main():
    with open(sys.argv[1]) as f:
        lines = [parse_line(s) for s in f]

    lines = sorted([
        ((categorize(cards), *[VALUE[c] for c in cards]), cards, bid)
        for cards, bid in lines
    ])
    for i, (key, cards, bid) in enumerate(lines):
        print(i + 1, cards, bid, key)

    print(sum((i + 1) * bid for i, (_, _, bid) in enumerate(lines)))


main()
