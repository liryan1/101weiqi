import json
from itertools import cycle
from helpers import make_fat, is_fat, to_lower_left, is_in_lower_left

BOOK = r"《入门棋书》"
input_file = "/".join(["data/json", f"{BOOK}.json"])
output_folder = "data/sgf"
SGF_HEADER = "GM[1]FF[4]SZ[19]"


def transform(black_stones, white_stones, solution):
    """Transform the stones and solution so they match
    """
    solution = to_lower_left(make_fat(solution), 19)
    if not is_in_lower_left(black_stones + white_stones):
        black_stones = to_lower_left(black_stones, 19)
        white_stones = to_lower_left(white_stones, 19)

    if not is_fat(black_stones + white_stones):
        black_stones = make_fat(black_stones)
        white_stones = make_fat(white_stones)
    return black_stones, white_stones, solution


def generate_sgf_node(problem) -> str:
    black_stones = problem.get("Black stones", [])
    white_stones = problem.get("White stones", [])
    solution = problem.get("Solution", [])

    black_stones, white_stones, solution = \
        transform(black_stones, white_stones, solution)

    black_stones_str = "AB" + "".join(f"[{c}]" for c in black_stones)
    white_stones_str = "AW" + "".join(f"[{c}]" for c in white_stones)
    start_player = problem.get("Start", "B")
    comments = problem.get("Comments", "")

    root = f"(;{black_stones_str}{white_stones_str}C[{comments}]"

    moveCycle = cycle(["B", "W"])
    if start_player == "W":
        next(moveCycle)
    if solution:
        main_line = "".join(
            f";{next(moveCycle)}[{move}]" for move in solution
        )
        root += main_line

    root += ")"
    return root


def convert_go_problems_to_sgf(data):
    sgf = []
    for problem in list(data.values())[30:40]:
        sgf.append(generate_sgf_node(problem))
    return "(;" + SGF_HEADER + "\n".join(sgf) + ")"


def main() -> None:
    with open(input_file, "r") as f:
        jsonProblems = json.load(f)
    print(f"Loaded {len(jsonProblems)} problems from {input_file}")
    sgf_output = convert_go_problems_to_sgf(jsonProblems)
    # print(sgf_output)

    output_file = f"{output_folder}/{BOOK.split("/")[-1]}.sgf"
    print(f"Saving output to '{output_file}'")
    with open(f"{output_folder}/{BOOK.split("/")[-1]}.sgf", "w") as f:
        f.write(sgf_output)


if __name__ == "__main__":
    main()
