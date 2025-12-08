"""Advent of Code 2025 Day 6."""
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
    rows = [line.split() for line in lines]
    return list(zip(*rows))


def calculate_columns(cols):
    """Calculate the result of each column."""
    results = []
    for col in cols:
        op = col[-1]
        if op not in ('+', '*'):
            print(f"Skipping malformed column. No operator found: {col}")
            continue
        try:
            col_nums = [int(i) for i in col[:-1]]
        except ValueError as ve:
            print(f"Error parsing column: {col=}")
            raise ve
        match op:
            case '+':
                results.append(
                    reduce(operator.add, col_nums)
                )
            case '*':
                results.append(
                    reduce(operator.mul, col_nums)
                )
            case _:
                raise ValueError("Invalid column: Didn't end with op.")
    return results


def main():
    """Run the main body of the script."""
    # lines = get_input("p6-sample-input.txt")
    lines = get_input("p6-full-input.txt")
    cols = get_columns(lines)
    results = calculate_columns(cols)
    print(f"{results=}")
    print(f"{sum(results)=}")


if __name__ == "__main__":
    main()
