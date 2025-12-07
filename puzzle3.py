"""Advent of Code puzzle3 part 1 and part 2."""


def gen_input(filepath):
    """Generate the input."""
    with open(filepath, 'r') as f:
        for line in f:
            yield line.strip()


def get_max_subsequence_joltages(line: str, count: int = 12) -> tuple[int]:
    """Get max subsequence joltages for part 2."""
    current = 0
    result_digits = []
    line_len = len(line)
    # So start at, e.g., 12 and go down.
    for remaining_needed in range(count, 0, -1):
        # limit: e.g., 12 - 3 + 1 = 10
        limit = line_len - remaining_needed + 1
        window = line[current:limit]
        best = max(window)
        result_digits.append(best)
        # Just after the digit we picked.
        current += window.index(best) + 1
    return tuple(result_digits)


def get_two_joltages(line: str) -> tuple[int]:
    """Get the max 2 joltages from string."""
    max_first_joltage = 0
    max_second_joltage = 0
    boundary = 0
    for i in range(len(line) - 1):
        if int(line[i]) > max_first_joltage:
            boundary = i + 1
            max_first_joltage = int(line[i])
    for j in range(boundary, len(line)):
        if int(line[j]) > max_second_joltage:
            max_second_joltage = int(line[j])
    return (max_first_joltage, max_second_joltage)


def make_final_joltage(joltages: tuple[int]) -> str:
    """Put joltages into a single string."""
    return ''.join(map(str, joltages))


def get_total_output_joltage(lines: list, joltage_getter) -> int:
    """Get the total output joltage from lines."""
    joltages_str = []
    for line in lines:
        joltages_str.append(
            make_final_joltage(joltage_getter(line))
        )
    joltages_int = map(int, joltages_str)
    return sum(joltages_int)


def main():
    """Run the main body of the script."""
    lines = list(gen_input("p3-full-input.txt"))
    print("Part 1:")
    output_joltage = get_total_output_joltage(lines, get_two_joltages)
    print(f"\t{output_joltage=}")
    print("Part 2:")
    output_joltage = get_total_output_joltage(
        lines, get_max_subsequence_joltages
    )
    print(f"\t{output_joltage=}")


if __name__ == "__main__":
    main()
