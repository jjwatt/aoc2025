"""Advent of Code 2025: Puzzle 2, part 1 and part 2."""
import itertools
import re
from collections.abc import Iterable


def gen_str_ranges(filepath):
    """Read ranges from file."""
    with open(filepath, "r") as f:
        ranges = f.readline().split(',')
    for range in ranges:
        yield range.strip()


def range_from_str(range_str: str):
    """Generate values from a range string.

    Args:
        range_str: Like, "1-10"
    """
    start, end = map(int, range_str.split('-'))
    return range(start, end)


def is_invalid_id(num: int) -> bool:
    """Check the puzzle condition.

    Does 2nd half == 1st half?
    """
    s = str(num)
    mid = len(s) // 2
    return s[:mid] == s[mid:]


def gen_invalid_ids(ranges: Iterable):
    """Generate invalid ids for 1st part of puzzle."""
    ranges = map(range_from_str, ranges)
    all_ids = itertools.chain.from_iterable(ranges)
    return (i for i in all_ids if is_invalid_id(i))


def gen_invalid_ids2(ranges: Iterable):
    """Generate invalid ids for 2nd part of puzzle."""
    ranges = map(range_from_str, ranges)
    all_ids = itertools.chain.from_iterable(ranges)
    return (i for i in all_ids if re.match(r'(\d+)\1+$', str(i)))


def main():
    """Run the main body of the script."""
    invalid_ids1 = gen_invalid_ids(gen_str_ranges("input2.txt"))
    invalid_ids2 = gen_invalid_ids2(gen_str_ranges("input2.txt"))
    print(f"sum(invalid_ids1): {sum(invalid_ids1)}")
    print(f"sum(invalid_ids2): {sum(invalid_ids2)}")


if __name__ == "__main__":
    main()
