"""Advent of Code 2025 Day 10, part 1."""
import re
from collections import deque


def gen_input(filepath):
    """Generate the input."""
    with open(filepath, 'r') as f:
        for line in f:
            yield line.rstrip('\n')


def gen_parsed_strings(lines):
    """Generate extracted strings.

    Extract target pattern. e.g., ".##." and buton pattern. e.g.,
    ["0,3", "1,2"].
    """
    for line in lines:
        target_str = re.search(r'\[(.*?)\]', line).group(1)
        button_strs = re.findall(r'\((.*?)\)', line)
        yield target_str, button_strs


def gen_bitmasks(parsed_data):
    """Generate integer bitmasks from parsed string data."""
    for target_str, button_strs in parsed_data:
        target_mask = 0
        for idx, char in enumerate(target_str):
            if char == '#':
                target_mask |= (1 << idx)
        button_masks = []
        for button_str in button_strs:
            mask = 0
            if button_str:
                indices = [int(x) for x in button_str.split(',')]
            for idx in indices:
                mask |= (1 << idx)
            button_masks.append(mask)
        yield target_mask, button_masks


def gen_solutions(machines):
    """Generate the shortest path from 0 (all off) to target using BFS."""


def main():
    filename = "p10-sample-input.txt"
    parsed_strings = list(gen_parsed_strings(gen_input(filename)))
    print(f"{parsed_strings=}")
    machines = gen_bitmasks(parsed_strings)
    print(f"{list(machines)=}")


if __name__ == "__main__":
    main()
