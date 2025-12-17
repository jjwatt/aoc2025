"""Advent of Code 2025 Day 10, part 1 and part 2."""
import re
from collections import deque


from z3 import Optimize, Int, Sum, sat


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


def gen_parsed_joltage_strings(lines):
    """Generate extracted joltage strings and buttons.

      Extract joltages and buttons.
      e.g., ("3,5,4,7", ["0,3", "1,2"]).
    """
    for line in lines:
        joltage_str = re.search(r'\{(.*?)\}', line).group(1)
        button_strs = re.findall(r'\((.*?)\)', line)
        yield joltage_str, button_strs


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


def gen_target_solutions(machines):
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


def gen_vectors(parsed_strings):
    """Generate vectors."""
    for joltage_str, button_strs in parsed_strings:
        target_vec = tuple(map(int, joltage_str.split(',')))
        num_counters = len(target_vec)

        # Convert Buttons "(1, 3)" -> (0, 1, 0, 1)
        button_vecs = []
        for button_str in button_strs:
            vec = [0] * num_counters
            if button_str:
                indices = [int(x) for x in button_str.split(',')]
                for idx in indices:
                    if idx < num_counters:
                        vec[idx] = 1
            button_vecs.append(tuple(vec))
        yield target_vec, button_vecs


def gen_z3_solutions(machines):
    """Use Z3 solver to yield the answer for each machine."""
    for idx, (target, buttons) in enumerate(machines):
        opt = Optimize()
        # "b_0", "b_1", etc. represent press counts.
        press_counts = [Int(f'b_{k}') for k in range(len(buttons))]

        for x in press_counts:
            opt.add(x >= 0)

        num_dims = len(target)
        for dim in range(num_dims):
            # Sum of (button_contribution * press_count) == target_value
            dim_sum = Sum([
                buttons[k][dim] * press_counts[k]
                for k in range(len(buttons))
            ])
            # Dimension must match target.
            opt.add(dim_sum == target[dim])

        # Minimize total presses.
        opt.minimize(Sum(press_counts))

        if opt.check() == sat:
            model = opt.model()
            # Extract result as a standard Python int.
            result = sum(model[x].as_long() for x in press_counts)
            yield result
        else:
            print(f"Machine {idx + 1}: Impossible!")
            yield 0


def main():
    # filename = "p10-sample-input.txt"
    filename = "p10-full-input.txt"
    print(f"Part 1:")
    solutions = gen_target_solutions(
        gen_bitmasks(
            gen_parsed_strings(
                gen_input(filename)
            )
        )
    )
    total_presses = sum(solutions)
    print(f"\tTotal: {total_presses}")
    print("Part 2:")
    joltage_solutions = gen_z3_solutions(
        gen_vectors(
            gen_parsed_joltage_strings(
                gen_input(filename)
            )
        )
    )
    total_joltage_presses = sum(joltage_solutions)
    print(f"\tTotal: {total_joltage_presses}")

if __name__ == "__main__":
    main()
