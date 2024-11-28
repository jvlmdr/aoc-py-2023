import re

COUNT_PATTERN = re.compile(r'(\d+) ([a-z]+)$')
DECK = {'red': 12, 'green': 13, 'blue': 14}


def parse_game(line):
    m = re.match(r'Game (\d+): (.*)', line)
    game_id = int(m[1])
    draws = m[2].split('; ')
    return game_id, [parse_draw(s) for s in draws]


def parse_draw(draw):
    counts = list(parse_count(s) for s in draw.split(', '))
    out = {}
    for k, v in counts:
        out[k] = out.get(k, 0) + v
    return out


def parse_count(count):
    m = COUNT_PATTERN.match(count)
    return (m[2], int(m[1]))


def check_game(game):
    game_id, draws = game
    return all(
        all(count <= DECK.get(color) for color, count in draw.items())
        for draw in draws
    )


def main():
    with open('input.txt') as f:
        lines = f.readlines()

    games = [parse_game(line) for line in lines]
    print(sum(
        game[0] for game in games if check_game(game)
    ))


if __name__ == '__main__':
    main()
