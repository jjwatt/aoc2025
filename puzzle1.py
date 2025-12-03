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


def gen_inputs(filepath):
    with open(filepath, "r") as f:
        for line in f:
            yield line


def gen_outputs(inputs):
    return itertools.accumulate(inputs, move_dial, initial=50)


def main():
    gen_results = gen_outputs(gen_inputs("input.txt"))
    gen_zeroes = (i for i in gen_results if i == 0)
    count_zeroes = len(list(gen_zeroes))
    print(f"{count_zeroes}")


if __name__ == "__main__":
    main()
