r'''

'''

import collections
import functools
import itertools
from pprint import pprint
import re
import sys

import numpy as np
from tqdm import tqdm


def main():
    with open(sys.argv[1]) as f:
        lines = [s.rstrip() for s in f.readlines()]


if __name__ == '__main__':
    main()
