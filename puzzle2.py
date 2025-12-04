"""Advent of Code 2025: Puzzle 2, part 1 and part 2."""
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
    try:
        start_str, end_str = range_str.split('-')
        start, end = int(start_str), int(end_str)
    except ValueError as ve:
        print(f"Bad range string: {ve}")
    return range(start, end)


def gen_ranges(ranges_str: Iterable):
    """Generate ranges of ids."""
    for range_str in ranges_str:
        yield range_from_str(range_str)


def gen_invalid_ids(ranges: Iterable):
    """Generate invalid ids for 1st part of puzzle."""
    for range in ranges:
        for id in range:
            str_id = str(id)
            str_id_len = len(str_id)
            half_len = str_id_len // 2
            if str_id[half_len:] == str_id[:half_len]:
                yield id


def gen_invalid_ids2(ranges: Iterable):
    """Generate invalid ids for 2nd part of puzzle."""
    for range in ranges:
        for id in range:
            if re.match(r'(\d+)\1+$', str(id)):
                yield id


def main():
    """Run the main body of the script."""
    invalid_ids = gen_invalid_ids2(
        gen_ranges(gen_str_ranges("input2.txt"))
    )
    print(f"sum(invalid_ids): {sum(invalid_ids)}")


if __name__ == "__main__":
    main()
