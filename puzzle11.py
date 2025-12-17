"""Advent of code Day 11, part 1."""
from functools import cache


def parse_graph(lines):
    """Parse the graph from the input."""
    adj = {}
    for line in lines:
        src, dsts = line.split(": ")
        adj[src] = dsts.split(' ')
    return adj


def main():
    pass


if __name__ == "__main__":
    main()
