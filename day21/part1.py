import sys
from collections import deque

def parse_garden_map(input_map):
    garden_map = [list(line.strip()) for line in input_map.strip().split('\n')]

    for r, row in enumerate(garden_map):
        for c, cell in enumerate(row):
            if cell == 'S':
                garden_map[r][c] = '.'
                return garden_map, (r, c)

    raise ValueError("No starting position found")

def count_garden_plots(garden_map, start, steps):
    rows, cols = len(garden_map), len(garden_map[0])

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    current_plots = {start}

    for _ in range(steps):
        next_plots = set()

        for plot in current_plots:
            for dr, dc in directions:
                new_r, new_c = plot[0] + dr, plot[1] + dc

                check_r, check_c = new_r % rows, new_c % cols

                if garden_map[check_r][check_c] == '.':
                    next_plots.add((new_r, new_c))

        current_plots = next_plots

    return len(current_plots)

def solve_step_counter(input_map, steps=64):
    garden_map, start = parse_garden_map(input_map)
    return count_garden_plots(garden_map, start, steps)


def main():
    # Read input from file specified in command line argument
    with open(sys.argv[1], 'r') as file:
        puzzle_input = file.read()

    # Solve the puzzle
    print("Solution:", solve_step_counter(puzzle_input))


main()