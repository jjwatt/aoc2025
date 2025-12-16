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
    for idx, (target, buttons) in enumerate(machines):
        queue = deque([(0, 0)])
        visited = {0}
        solved = False
        while queue:
            current_state, presses = queue.popleft()
            if current_state == target:
                # print(f"Machine {idx+1}: Solved in {presses}")
                yield presses
                solved = True
                break
            for button_mask in buttons:
                new_state = current_state ^ button_mask
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, presses + 1))
        if not solved:
            print(f"Machine {idx+1}: Impossilbe!")
            yield 0

def main():
    # filename = "p10-sample-input.txt"
    filename = "p10-full-input.txt"
    solutions = gen_solutions(
        gen_bitmasks(
            gen_parsed_strings(
                gen_input(filename)
            )
        )
    )
    total_presses = sum(solutions)
    print(f"Part1:")
    print(f"\tTotal: {total_presses}")


if __name__ == "__main__":
    main()
