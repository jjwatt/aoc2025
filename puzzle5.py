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


def merge_ranges(ranges):
    """Merge ranges like (12, 18), (16, 20)."""
    merged_ranges = []
    sorted_ranges = sorted(ranges)
    if sorted_ranges:
        cur_start, cur_end = sorted_ranges[0]
        for next_start, next_end in sorted_ranges[1:]:
            if next_start <= cur_end:
                cur_end = max(cur_end, next_end)
            else:
                merged_ranges.append((cur_start, cur_end))
                cur_start, cur_end = next_start, next_end
        merged_ranges.append((cur_start, cur_end))
    return merged_ranges


def main():
    """Run the main body of the script."""
    ranges = list(gen_range_values(gen_str_ranges("p5-full-input.txt")))
    count_fresh = 0
    for i in gen_ingredients("p5-full-input.txt"):
        if is_fresh(i, ranges):
            count_fresh += 1
    print("Part 1:")
    print(f"\t{count_fresh=}")
    print("Part 2:")
    merged_ranges = merge_ranges(ranges)
    total_fresh = 0
    for start, end in merged_ranges:
        total_fresh += (end - start + 1)
    print(f"\t{total_fresh=}")


if __name__ == "__main__":
    main()
