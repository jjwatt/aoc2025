"""Advent of Code puzzle4 part 1."""
import copy


def gen_input(filepath):
    """Generate the input."""
    with open(filepath, 'r') as f:
        for line in f:
            yield line.strip()


def build_grid(lines):
    """Build the grid from lines of text."""
    grid = []
    for line in lines:
        row = list(line)
        grid.append(row)
    return grid


def check_neighbors(grid, row, col):
    """Check adjacent grid cells to see if they meet requirements.

    Check to see if adjacent grid cells have fewer than 4 @s.
    """
    rows = len(grid)
    cols = len(grid[0])
    neighbors = 0
    deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    for dr, dc in deltas:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] == '@':
                neighbors += 1
    return neighbors < 4


def check_grid_accessible(grid):
    """Check for the number of accessible slots in the grid."""
    rows = len(grid)
    cols = len(grid[0])
    accessible = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '@':
                if check_neighbors(grid, row, col):
                    accessible += 1
    return accessible


def get_removable(grid):
    """Check for the accessible slots in the grid."""
    rows = len(grid)
    cols = len(grid[0])
    removable = []
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '@':
                if check_neighbors(grid, row, col):
                    removable.append((row, col))
    return removable


def check_total_removed(grid):
    """Find the total number we can remove by repeating removals."""
    mygrid = copy.copy(grid)
    total_removed = 0
    while True:
        removable = get_removable(mygrid)
        if not removable:
            break
        total_removed += len(removable)
        for row, col in removable:
            mygrid[row][col] = '.'
    return total_removed


def main():
    """Run the main body of the script."""
    lines = list(gen_input("p4-full-input.txt"))
    grid = build_grid(lines)
    print("Part1:")
    accessible = check_grid_accessible(grid)
    print(f"\t{accessible=}")
    print("Part2:")
    total_removed = check_total_removed(grid)
    print(f"\t{total_removed=}")


if __name__ == "__main__":
    main()
