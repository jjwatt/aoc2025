"""Advent of Code 2025 Day 9."""
import itertools


def get_input(filepath):
    """Generate the input."""
    lines = []
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    return lines


def parse_lines(lines):
    """Parse lines into coordinate tuples."""
    coords = []
    for line in lines:
        tup_coords_ints = tuple(map(int, line.split(",")))
        coords.append(tup_coords_ints)
    return coords


def get_areas(coords):
    """Get areas of squares for all coordinates."""
    areas = []
    for (x1, y1), (x2, y2) in itertools.combinations(coords, 2):
        width = abs(x1 - x2) + 1
        height = abs(y1 - y2) + 1
        area = width * height
        areas.append(area)
    return areas


def is_center_inside(min_x, max_x, min_y, max_y, edges):
    """Return true if the center of the rectangle is inside the polygon."""
    cx = (min_x, max_x) / 2
    cy = (min_y, max_y) / 2
    crossings = 0
    for (x1, y1), (x2, y2) in edges:
        # We only care about vertical edges for a horizontal ray cast.
        # A horizontal ray doesn't cross, but overlaps or misses.
        if x1 == x2:
            # Is the edge to the right of the center?
            if x1 > cx:
                # Does center y fall within edge's y range?
                edge_y_min, edge_y_max = min(y1, y2), max(y1, y2)
                # Standard raycasting rule: include bottom, exclude top.
                if edge_y_min <= cy < edge_y_max:
                    crossings += 1
    # Odd number of crossings = inside.
    # Even number of crossings = outside.
    return crossings % 2 == 1


def hits_any_wall():
    """Return true if the points hit any of the walls/edges."""
    pass


def get_areas2(coords):
    """Get areas of squares inside walls."""
    edges = build_edges(coords)
    areas = []
    for (x1, y1), (x2, y2) in itertools.combinations(coords, 2):
        # Define rectangle boundaries.
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        if is_center_inside(min_x, max_x, min_y, max_y, edges):
            if not hits_any_wall(min_x, max_x, min_y, max_y, edges):
                width = (max_x - min_x) + 1
                height = (max_y - min_y) + 1
                areas.append(width * height)


def build_edges(coords):
    """Build the walls."""
    edges = []
    num_points = len(coords)
    for point in range(num_points):
        p1 = coords[point]
        # Wrap around to the start index.
        p2 = coords[(point + 1) % num_points]
        edges.append((p1, p2))
    return edges


def main():
    """Run the main body of the script."""
    # lines = list(get_input("p9-sample-input.txt"))
    lines = list(get_input("p9-full-input.txt"))
    coords = parse_lines(lines)
    areas = get_areas(coords)
    print("Part 1:")
    print(f"\t{sorted(areas, reverse=True)[0]=}")


if __name__ == "__main__":
    main()
