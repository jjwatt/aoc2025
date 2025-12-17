"""Advent of Code 2025 Day 10, part 1 and part 2."""
import heapq
import math
import re
from collections import deque
from itertools import combinations


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


def gen_joltage_solutions_naive(machines):
    """Generate answer for each machine with BFS."""
    for idx, (target, buttons) in enumerate(machines):
        start_node = tuple([0] * len(target))
        queue = deque([(start_node, 0)])
        visited = {start_node}
        solved = False
        while queue:
            current_vec, presses = queue.popleft()
            if current_vec == target:
                # print(f"Machine {idx + 1} solved in {presses} presses")
                yield presses
                solved = True
                break
            for button_vec in buttons:
                # Vector addition.
                new_vec = tuple(c + b for c,b in zip(current_vec, button_vec))
                # Pruning: if we overshoot target in ANY dimension, stop.
                if any(n > t for n,t in zip(new_vec, target)):
                    continue
                if new_vec not in visited:
                    visited.add(new_vec)
                    queue.append((new_vec, presses + 1))
        if not solved:
            print(f"Machine {idx + 1}: Impossible!")
            yield 0


def gen_joltage_solutions_astar(machines):
    """Generate joltage solutions with A* search."""
    for idx, (target, buttons) in enumerate(machines):
        num_dims = len(target)
        start_node = tuple([0] * num_dims)
        # max_per_dim[k] = the biggest number any single button adds to k
        max_per_dim = []
        for d in range(num_dims):
            # Find max.
            # Default to 1 to avoid div by 0 errors.
            m = max(button[d] for button in buttons) if buttons else 1
            max_per_dim.append(m if m > 0 else 1)
        def heuristic(current_vec):
            """Estimate minimum presses remaining."""
            max_needed = 0
            for d in range(num_dims):
                diff = target[d] - current_vec[d]
                if diff > 0:
                    needed = math.ceil(diff / max_per_dim[d])
                    if needed > max_needed:
                        max_needed = needed
            return max_needed
        # Priority Queue:
        # (Estimated total cost, presses so far, state)
        # Estimated total cost = presses so far + heuristic estimate
        start_h = heuristic(start_node)
        pq = [(start_h, 0, start_node)]

        # Track the best cost to reach a state to avoid loops/redundancy.
        min_presses_to_state = {start_node: 0}
        solved = False
        while pq:
            est_total, presses, current_vec = heapq.heappop(pq)
            # If we found a path to target, A* guarantees it's the shortest.
            if current_vec == target:
                yield presses
                solved = True
                break
            # Optimization: If we found a faster way already, skip
            # the slower path.
            if presses > min_presses_to_state.get(current_vec, float('inf')):
                continue
            for btn_vec in buttons:
                new_vec = tuple(c + b for c,b in zip(current_vec, btn_vec))
                if any(n > t for n,t in zip(new_vec, target)):
                    continue
                new_cost = presses + 1
                if new_cost < min_presses_to_state.get(new_vec, float('inf')):
                    min_presses_to_state[new_vec] = new_cost
                    h = heuristic(new_vec)
                    priority = new_cost + h
                    heapq.heappush(pq, (priority, new_cost, new_vec))
        if not solved:
            print(f"Machine {idx + 1}: Impossible!")
            yield 0


def solve_subset(buttons, target):
    """
    Solve Ax = b where A is formed by button vectors.
    Returns non-negative integer solution if exists, else None.
    """
    n = len(target)
    m = len(buttons)

    # Build augmented matrix [A | b]
    # A[i][j] = buttons[j][i] (transpose for easier solving)
    matrix = []
    for i in range(n):
        row = [buttons[j][i] for j in range(m)] + [target[i]]
        matrix.append(row)

    # Gaussian elimination with back substitution
    # First, make it upper triangular
    for col in range(min(n, m)):
        # Find pivot
        pivot_row = None
        for row in range(col, n):
            if matrix[row][col] != 0:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        # Swap rows
        matrix[col], matrix[pivot_row] = matrix[pivot_row], matrix[col]

        # Eliminate below
        for row in range(col + 1, n):
            if matrix[row][col] != 0:
                # Use integer operations to avoid fractions
                lcm_factor = matrix[row][col]
                pivot_factor = matrix[col][col]

                for c in range(m + 1):
                    matrix[row][c] = matrix[row][c] * pivot_factor - matrix[col][c] * lcm_factor
    
    # Back substitution
    solution = [0] * m
    
    for i in range(min(n, m) - 1, -1, -1):
        # Find the leading coefficient
        leading_col = None
        for c in range(m):
            if matrix[i][c] != 0:
                leading_col = c
                break

        if leading_col is None:
            # Check if this row is consistent (0 = 0)
            if matrix[i][-1] != 0:
                return None  # Inconsistent
            continue

        # Calculate solution[leading_col]
        val = matrix[i][-1]
        for c in range(leading_col + 1, m):
            val -= matrix[i][c] * solution[c]

        if val % matrix[i][leading_col] != 0:
            return None  # Not an integer solution

        solution[leading_col] = val // matrix[i][leading_col]

        if solution[leading_col] < 0:
            return None  # Negative solution

    # Verify solution
    for i in range(n):
        total = sum(buttons[j][i] * solution[j] for j in range(m))
        if total != target[i]:
            return None

    return solution

def solve_linear_system(buttons, target):
    """
    Solve the system: find non-negative integers x_i such that
    sum(x_i * button_i[j]) = target[j] for all j

    Minimizing sum(x_i).

    Strategy: Try all combinations of buttons up to size = num_counters,
    solve the exact system, check if solution is non-negative integers.
    """
    n_counters = len(target)
    n_buttons = len(buttons)

    # Try increasingly larger subsets of buttons
    for subset_size in range(1, n_buttons + 1):
        for button_indices in combinations(range(n_buttons), subset_size):
            # Build matrix A where A[counter][button] = 1 if button affects counter
            # We want: A * x = target
            selected_buttons = [buttons[i] for i in button_indices]

            # Try to solve this system
            solution = solve_subset(selected_buttons, target)

            if solution is not None:
                # Map back to full button array
                full_solution = [0] * n_buttons
                for i, btn_idx in enumerate(button_indices):
                    full_solution[btn_idx] = solution[i]
                return sum(full_solution)
    
    return None  # No solution found


def gen_joltage_solutions(machines):
    """Generate joltage solutions using linear algebra."""
    for idx, (target, buttons) in enumerate(machines):
        if not buttons or not target:
            yield 0
            continue

        result = solve_linear_system(buttons, target)

        if result is not None:
            yield result
        else:
            print(f"Machine {idx + 1}: No solution found!")
            yield 0


def main():
    # filename = "p10-sample-input.txt"
    filename = "p10-full-input.txt"
    print(f"Part 1:")
    solutions = gen_solutions(
        gen_bitmasks(
            gen_parsed_strings(
                gen_input(filename)
            )
        )
    )
    total_presses = sum(solutions)
    print(f"\tTotal: {total_presses}")
    print("Part 2:")
    joltage_solutions = gen_joltage_solutions(
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
