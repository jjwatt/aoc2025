"""Advent of Code 2025 Day 9."""
import itertools

def get_input(filepath):
    """Generate the input."""
    lines = []
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    return lines


def parse_lines(lines):
    coords = []
    for line in lines:
        tup_coords_ints = tuple(map(int, line.split(",")))
        coords.append(tup_coords_ints)
    return coords


def get_areas(coords):
    areas = []
    for (x1, y1), (x2, y2) in itertools.combinations(coords, 2):
        width = abs(x1 - x2) + 1
        height = abs(y1 - y2) + 1
        area = width * height
        areas.append(area)
    return areas


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
