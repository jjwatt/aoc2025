"""Advent of Code 2025 Day 8."""
import itertools
import math


class UnionFind:
    """Disjoint Set Union/Union Find data structure."""

    def __init__(self, total_nodes):
        """Initialize a UnionFind."""
        self.parent = list(range(total_nodes))
        self.size = [1] * total_nodes
        self.num_components = total_nodes

    def find(self, node_id):
        """Find the root representative of node with Path Compression."""
        if self.parent[node_id] != node_id:
            # Recursively find the root and point node directly to it.
            # This flattens the tree, making lookups O(1).
            self.parent[node_id] = self.find(self.parent[node_id])
        return self.parent[node_id]

    def union(self, node_a, node_b):
        """Unite circuits containing node_a and node_b.

        Args:
            node_a: The first node.
            node_b: The second node.
        Returns:
            True if a merge happened, False if already connected.
        """
        root_a = self.find(node_a)
        root_b = self.find(node_b)
        if root_a != root_b:
            # Merge circuit b into circuit a.
            self.parent[root_b] = root_a
            # Add the size of the absorbed circuit to the new root.
            self.size[root_a] += self.size[root_b]
            self.num_components -= 1
            return True
        return False


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
    """Generate combinations of nodes."""
    for (i, node_a), (j, node_b) in itertools.combinations(
        enumerate(nodes), 2
    ):
        yield (i, node_a), (j, node_b)


def gen_distances(combinations):
    """Generate distances between nodes."""
    for (i, node_a), (j, node_b) in combinations:
        distance_sq = sum((a - b)**2 for a, b in zip(node_a, node_b))
        distance = math.sqrt(distance_sq)
        yield (distance, i, j)


def main():
    """Run the main body of the script."""
    input_file = "p8-full-input.txt"
    print("Part 1:")
    nodes = list(gen_nodes(gen_input(input_file)))
    sorted_edges = sorted(gen_distances(gen_combinations(nodes)))
    uf = UnionFind(len(nodes))
    if input_file == "p8-sample-input.txt":
        limit = 10
    else:
        limit = 1000
    for _, u, v in sorted_edges[:limit]:
        uf.union(u, v)
    # Filter the root nodes to get valid circuit sizes.
    circuit_sizes = [
        uf.size[i] for i in range(
            len(nodes)
        ) if uf.parent[i] == i
    ]
    circuit_sizes.sort(reverse=True)
    # Safety check in case there are fewer than 3 circuits
    if len(circuit_sizes) >= 3:
        result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
        print(f"\tTop 3 sizes: {circuit_sizes[:3]}")
        print(f"\tAnswer: {result}")
    else:
        print("Not enough circuits formed!")
    print("Part 2:")
    uf = UnionFind(len(nodes))
    for _, u, v in sorted_edges:
        if uf.union(u, v):
            if uf.num_components == 1:
                print(f"\tGraph fully connected by connecting {u} and {v}")
                x1 = nodes[u][0]
                x2 = nodes[v][0]
                print(f"\tAnser: {x1 * x2}")
                break
    

if __name__ == "__main__":
    main()
