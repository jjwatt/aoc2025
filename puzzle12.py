"""Advent of Code 2025, Day 12."""


def gen_lines(filepath):
    """Generate lines to parse."""
    with open(filepath, 'r') as f:
        for line in f:
            yield line

def gen_shapes(lines):
    """Consume lines from iterator to parse shapes."""
    current_id = None
    current_coords = []
    row = 0

    for line in lines:
        if not line:
            if current_id is None:
                yield current_id, normalize(current_coords)
                current_id = None
                current_coords = []
                row = 0
            continue



