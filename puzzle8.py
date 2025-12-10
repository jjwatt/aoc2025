"""Advent of Code 2025 Day 8."""
import itertools
import math

def gen_input(filepath):
    """Generate the input."""
    with open(filepath, 'r') as f:
        for line in f:
            yield line.rstrip('\n')


def gen_nodes(lines):
    """Generate list of "x, y, z" into list of (x, y, z)."""
    for line in lines:
        yield tuple(map(int, line.split(",")))


def gen_combinations(nodes):
    for (i, node_a), (j, node_b) in itertools.combinations(enumerate(nodes), 2):
        yield (i, node_a), (j, node_b)

def gen_edges(combinations):
    for (i, node_a), (j, node_b) in combinations:
        distance_sq = sum((a - b)**2 for a, b in zip(node_a, node_b))
        distance = math.sqrt(distance_sq)
        yield (distance, i, j)

def main():
    """Run the main body of the script."""
    lines = list(gen_input("p8-sample-input.txt"))
    # lines = list(get_input("p7-full-input.txt"))
    print(f"{lines=}")
    nodes = list(gen_nodes(lines))
    print(f"{nodes=}")
    sorted_edges = sorted(list(gen_edges(gen_combinations(nodes))))
    print(f"{sorted_edges=}")

if __name__ == "__main__":
    main()
 
