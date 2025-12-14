"""Advent of Code 2025 Day 10, part 1."""
import re

def get_input(filepath):
    """Generate the input."""
    lines = []
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    return lines


def get_targets(lines):
    """Get the target strings."""
    targets = []
    for line in lines:
        target = re.search(r'\[(.*?)\]', line).group(1)
        targets.append(target)
    return targets


def get_buttons(lines):
    all_buttons = []
    for line in lines:
        buttons = re.findall(r'\((.*?)\)', line)
        all_buttons.append(buttons)
    return all_buttons


def main():
    filename = "p10-sample-input.txt"
    lines = get_input(filename)
    print(f"{lines=}")
    targets = get_targets(lines)
    print(f"{targets=}")
    buttons = get_buttons(lines)
    print(f"{buttons=}")
    

if __name__ == "__main__":
    main()
