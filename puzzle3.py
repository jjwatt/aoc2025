from collections.abc import Iterable

def gen_input(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            yield line.strip()


def get_joltages(line: str):
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


def make_final_joltage(joltages: tuple[int]):
    return ''.join(map(str, joltages))


def get_total_output_joltage(lines: list):
    joltages_str = []
    for line in lines:
        joltages_str.append(
            make_final_joltage(get_joltages(line))
        )
    joltages_int = map(int, joltages_str)
    return sum(joltages_int)


def main():
    lines = list(gen_input("p3-full-input.txt"))
    output_joltage = get_total_output_joltage(lines)
    print(f"{output_joltage=}")

if __name__ == "__main__":
    main()
