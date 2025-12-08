"""Advent of Code 2025 Day 6 part 2."""


def get_input(filepath):
    """Generate the input."""
    lines = []
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    return lines


def build_grid(lines):
    """Build the grid from lines of text."""
    grid = []
    for line in lines:
        row = list(line)
        grid.append(row)
    return grid


def solve_part1(grid):
    """Find number of activated splitters."""
    rows = len(grid)
    cols = len(grid[0])

    start_col = -1
    for c in range(cols):
        if grid[0][c] == 'S':
            start_col = c
            break
    else:
        raise ValueError("No start column found!")

    queue = [(1, start_col)]
    activated_splitters = set()
    while queue:
        r, c = queue.pop(0)
        while r < rows:
            # Left/Right wall bounds.
            if not (0 <= c < cols):
                break
            char = grid[r][c]
            if char == '^':
                if (r, c) not in activated_splitters:
                    activated_splitters.add((r, c))
                    # Create two new beams.
                    queue.append((r + 1, c - 1))
                    queue.append((r + 1, c + 1))
                break
            # If it's empty, increase row count.
            r += 1
    return len(activated_splitters)


def main():
    """Run the main body of the script."""
    # lines = list(get_input("p7-sample-input.txt"))
    lines = list(get_input("p7-full-input.txt"))
    grid = build_grid(lines)
    # print(f"{lines=}")
    # print(f"{grid=}")
    activated_splitters_count = solve_part1(grid)
    print(f"{activated_splitters_count=}")


if __name__ == "__main__":
    main()
