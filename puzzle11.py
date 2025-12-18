"""Advent of code Day 11, part 1 and part 2."""
from functools import cache


def gen_lines(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            yield line


def parse_graph(lines):
    """Parse the graph from the input."""
    adj = {}
    for line in lines:
        src, dsts = line.rstrip('\n').split(": ")
        adj[src] = dsts.split(' ')
    return adj


def count_paths(graph, start_node, end_node):
    """Count the paths through the graph."""
    @cache
    def dfs(current_node):
        if current_node == end_node:
            return 1
        if current_node not in graph:
            return 0
        total = 0
        for neighbor in graph[current_node]:
            total += dfs(neighbor)
        return total
    return dfs(start_node)


def main():
    filepath = "p11-sample-input.txt"
    # filepath = "p11-full-input.txt"
    graph = parse_graph(gen_lines(filepath))
    print("Part 1:")
    total_paths = count_paths(graph, "you", "out")
    print(f"\tTotal Paths: {total_paths}")
    filepath = "p11-sample-input2.txt"
    graph = parse_graph(gen_lines(filepath))
    print("Part 2:")
    total_paths = count_paths(graph, "svr", "out")
    print(f"\tTotal Paths: {total_paths}")


if __name__ == "__main__":
    main()
