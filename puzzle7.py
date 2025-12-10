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


def solve_part2(lines):
    """Solve part2 with multiple timelines."""
    rows = len(lines)
    cols = max(len(line) for line in lines)

    # Cache to store the timeline count for each splitter.
    # Key: (row, col) of the splitter
    # Value: int (number of timelines resulting from this splitter)
    memo = {}

    def count_paths(r, c):
        """Recursive function to trace a beam downwards.

        Returns the number of timelines this specific beam results in.
        """
        curr_r, curr_c = r, c

        # Simulate the beam falling
        while curr_r < rows:
            # 1. Check Bounds (Left/Right)
            # If a beam flies off the side, it exits the manifold.
            # This counts as 1 valid timeline end.
            if not (0 <= curr_c < cols):
                return 1
            char = lines[curr_r][curr_c]
            # 2. Check for Splitter
            if char == '^':
                # If we have solved this splitter before, return the cached.
                if (curr_r, curr_c) in memo:
                    return memo[(curr_r, curr_c)]
                # Otherwise, calculate it: Left Path + Right Path
                # Beam emerges on the next row, shifted left (-1) and right (+1)
                left_paths = count_paths(curr_r + 1, curr_c - 1)
                right_paths = count_paths(curr_r + 1, curr_c + 1)
                total = left_paths + right_paths
                # Cache and return
                memo[(curr_r, curr_c)] = total
                return total
            # 3. Fall through empty space
            curr_r += 1
        # 4. Check Bottom
        # If the loop finishes, the beam fell out the bottom.
        # This counts as 1 valid timeline end.
        return 1

    # Find Start (S)
    start_pos = None
    for r, line in enumerate(lines):
        if 'S' in line:
            start_pos = (r, line.index('S'))
            break

    if not start_pos:
        return 0

    # Start the simulation from the row immediately below S
    return count_paths(start_pos[0] + 1, start_pos[1])


def main():
    """Run the main body of the script."""
    # lines = list(get_input("p7-sample-input.txt"))
    lines = list(get_input("p7-full-input.txt"))
    grid = build_grid(lines)
    # print(f"{lines=}")
    # print(f"{grid=}")
    activated_splitters_count = solve_part1(grid)
    print("Part 1:")
    print(f"\t{activated_splitters_count=}")
    print("Part 2:")
    total_timelines = solve_part2(lines)
    print(f"\t{total_timelines=}")


if __name__ == "__main__":
    main()
