r'''

'''

import collections
import functools
import heapq
import itertools
from pprint import pprint
import re
import sys

import numpy as np
from tqdm import tqdm


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]
    cost = np.asarray([[int(c) for c in s] for s in lines])
    m, n = cost.shape
    print(cost)
    queue = []

    def heuristic(pos):
        i, j = pos
        return abs(m - i) + abs(n - j)

    heapq.heappush(queue, (heuristic((0, 0)), 0, (0, 0), (0, 1)))
    heapq.heappush(queue, (heuristic((0, 0)), 0, (0, 0), (1, 0)))
    visited = set()

    while queue:
        _, path_cost, pos, direction = heapq.heappop(queue)
        if (pos, direction) in visited:
            continue
        visited.add((pos, direction))
        print(path_cost, pos, direction)
        if pos == (m-1, n-1):
            print(path_cost)
            break

        if direction[0] == 0:
            for sign in [1, -1]:
                step_cost = path_cost
                for i in range(1, 11):
                    step_pos = (pos[0] + sign * i, pos[1])
                    if not (0 <= step_pos[0] < m and 0 <= step_pos[1] < n):
                        break
                    step_cost += cost[step_pos]
                    if i < 4:
                        continue
                    rank = step_cost + heuristic(step_pos)
                    heapq.heappush(queue, (rank, step_cost, step_pos, (sign, 0)))
        elif direction[1] == 0:
            for sign in [1, -1]:
                step_cost = path_cost
                for i in range(1, 11):
                    step_pos = (pos[0], pos[1] + sign * i)
                    if not (0 <= step_pos[0] < m and 0 <= step_pos[1] < n):
                        break
                    step_cost += cost[step_pos]
                    if i < 4:
                        continue
                    rank = step_cost + heuristic(step_pos)
                    heapq.heappush(queue, (rank, step_cost, step_pos, (0, sign)))


if __name__ == '__main__':
    main()
