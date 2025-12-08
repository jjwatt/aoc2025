"""Advent of Code 2025 Day 6."""
import operator
from functools import reduce


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
    results = []
    for col in cols:
        op = col[-1]
        col_nums = [int(i) for i in col[:-1]]
        match op:
            case '+':
                # add
                results.append(
                    reduce(operator.add, col_nums)
                )
            case '*':
                # multiply
                results.append(
                    reduce(operator.mul, col_nums)
                )
            case _:
                raise ValueError("Invalid column: Didn't end with op.")
    return results


def main():
    """Run the main body of the script."""
    lines = get_input("p6-sample-input.txt")
    grid = make_grid(lines)
    cols = list(gen_column_values(grid))
    results = calculate_columns(cols)
    print(f"{results=}")
    print(f"{sum(results)=}")


if __name__ == "__main__":
    main()
