import itertools


def move_dial(dial_at, move):
    dir = move[0]
    clicks = int(move[1:])
    result = dial_at
    if dir == 'L':
        result = ((dial_at - clicks) % 100 + 100) % 100
    if dir == 'R':
        result = ((dial_at + clicks) % 100 + 100) % 100
    return result


def move_dial2(state, move):
    dir = move[0]
    clicks = int(move[1:])
    current_pos, current_hits = state
    hits_in_this_move = clicks // 100
    remainder = clicks % 100
    match dir:
        case 'L':
            new_pos = (current_pos - remainder) % 100
            if current_pos - remainder <= 0 and current_pos != 0:
                hits_in_this_move += 1
        case 'R':
            new_pos = (current_pos + remainder) % 100
            if current_pos + remainder >= 100:
                hits_in_this_move += 1
        case _:
            raise ValueError("Not a valid move")
    return (new_pos, current_hits + hits_in_this_move)


def gen_inputs(filepath):
    with open(filepath, "r") as f:
        for line in f:
            yield line


def gen_outputs(inputs):
    return itertools.accumulate(inputs, move_dial, initial=50)


def gen_outputs2(inputs):
    return itertools.accumulate(inputs, move_dial2, initial=(50, 0))


def main():
    gen_results = gen_outputs(gen_inputs("input.txt"))
    gen_zeroes = (i for i in gen_results if i == 0)
    count_zeroes = len(list(gen_zeroes))
    print(f"{count_zeroes}")

    gen_results2 = gen_outputs2(gen_inputs("input.txt"))
    print(f"2nd code: {list(gen_results2)[-1]}")

if __name__ == "__main__":
    main()
