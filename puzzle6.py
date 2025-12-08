"""Advent of Code 2025 Day 6."""


def get_input(filepath):
    """Generate the input."""
    lines = []
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    return lines


def make_grid(lines):
    """Pad lines with spaces to make an even grid."""
    max_width = max(len(line) for line in lines)
    grid = [line.ljust(max_width) for line in lines]
    return grid


def gen_column_values(grid):
    """Get the grid's columns."""
    height = len(grid)
    width = len(grid[0])
    step = 4
    for x in range(0, width, step):
        cur_col_values = []
        for y in range(height):
            chunk = grid[y][x: x + step]
            val = chunk.strip()
            if val:
                cur_col_values.append(val)
        yield cur_col_values


def calculate_columns(cols):
    """Calculate the result of each column."""
    for col in cols:
        op = col[-1]
        match op:
            case '+':
                # add
                pass
            case '*':
                # multiply
                pass
            case _:
                raise ValueError("Invalid column: Didn't end with op.")


def main():
    """Run the main body of the script."""
    lines = get_input("p6-sample-input.txt")
    print(f"{lines=}")
    grid = make_grid(lines)
    print(f"{grid=}")
    cols = list(gen_column_values(grid))
    print(f"{cols=}")


if __name__ == "__main__":
    main()
