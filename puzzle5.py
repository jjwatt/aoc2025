"""Advent of Code 2025 Day 5."""


def gen_str_ranges(filepath):
    """Generate the range strings."""
    with open(filepath, 'r') as f:
        for line in f:
            if line and '-' in line:
                yield line.strip()


def gen_range_values(str_ranges):
    """Generate the ranges start, end values."""
    for str_range in str_ranges:
        start, end = map(int, str_range.split('-'))
        yield (start, end)


def gen_ingredients(filepath):
    """Generate the ingredient strings."""
    with open(filepath, 'r') as f:
        for line in f:
            if '-' not in line:
                ingredient = line.strip()
                if ingredient:
                    yield int(ingredient)


def is_fresh(ingredient, ranges):
    """Check if the ingredient appears in the ranges."""
    for start, end in ranges:
        if start <= ingredient <= end:
            return True
    return False


def main():
    """Run the main body of the script."""
    ranges = list(gen_range_values(gen_str_ranges("p5-full-input.txt")))
    count_fresh = 0
    for i in gen_ingredients("p5-full-input.txt"):
        if is_fresh(i, ranges):
            count_fresh += 1
    print(f"{count_fresh=}")


if __name__ == "__main__":
    main()
