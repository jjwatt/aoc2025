"""Advent of Code 2025 Day 6 part 2."""
import operator
from functools import reduce


def get_input(filepath):
    """Generate the input."""
    lines = []
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    return lines


def get_columns(lines):
    """Split lines by whitespace and transpose rows to columns."""
    # Get max width of all lines.
    max_width = max(len(line) for line in lines)
    # Pad with spaces.
    grid = [line.ljust(max_width) for line in lines]
    return list(zip(*grid))


def calculate_columns(cols):
    """Calculate the result of each column, scan right to left."""
    total = 0
    cur_nums = []
    cur_op = None
    for col in reversed(cols):
        if all(c == ' ' for c in col):
            if cur_nums and cur_op:
                match cur_op:
                    case '+':
                        total += reduce(operator.add, cur_nums)
                    case '*':
                        total += reduce(operator.mul, cur_nums)
                    case _:
                        raise ValueError(f"Invalid operator: {cur_op}")
            cur_nums = []
            cur_op = None
            continue

        digits = "".join(col[:-1]).strip()
        if digits:
            cur_nums.append(int(digits))

        bottom_char = col[-1]
        if bottom_char in ('+', '*'):
            cur_op = bottom_char

    if cur_nums and cur_op:
        match cur_op:
            case '+':
                total += reduce(operator.add, cur_nums)
            case '*':
                total += reduce(operator.mul, cur_nums)
            case _:
                raise ValueError(f"Invalid operator: {cur_op}")
    return total


def main():
    """Run the main body of the script."""
    # lines = get_input("p6-sample-input.txt")
    lines = get_input("p6-full-input.txt")
    cols = get_columns(lines)
    results = calculate_columns(cols)
    print(f"{results=}")


if __name__ == "__main__":
    main()
