import json
from merge_variations import merge_variations, variations_to_sgf
from helpers import get_solution_distance, make_fat, is_fat, to_lower_left

BOOK = "tian_long_tu"
input_file = "/".join(["data/json", f"{BOOK}.json"])
output_folder = "data/sgf"
SGF_HEADER = "GM[1]FF[4]SZ[19]"

sgf_file_number = [0]


def get_comments(key: str, rank: str) -> str:
    return f"C[description: {key}\nrank: {rank.rstrip("+").lower()}]"


def transform(
    black_stones, white_stones, all_solutions
) -> tuple[list[str], list[str], list[list[str]]]:
    """Transform the stones and solution so they match"""
    black_stones, white_stones = to_lower_left(black_stones, white_stones)
    all_solutions = [to_lower_left(solution, [])[0] for solution in all_solutions]

    if not is_fat(black_stones + white_stones):
        black_stones = make_fat(black_stones)
        white_stones = make_fat(white_stones)

    fat_solutions = [make_fat(solution) for solution in all_solutions]
    origin_distance = sum(
        get_solution_distance(black_stones, white_stones, solution)
        for solution in all_solutions
    )
    fat_distance = sum(
        get_solution_distance(black_stones, white_stones, fat_solution)
        for fat_solution in fat_solutions
    )
    if (fat_distance) < origin_distance:
        all_solutions = fat_solutions

    return black_stones, white_stones, all_solutions


def generate_sgf_node(key, problem) -> str:
    black_stones = problem.get("Black stones", [])
    white_stones = problem.get("White stones", [])
    solution = problem.get("Solution", [])
    all_solutions = problem.get("Other variations", [])
    all_solutions.append(solution)

    black_stones, white_stones, all_solutions = transform(
        black_stones, white_stones, all_solutions
    )

    black_stones_str = "AB" + "".join(f"[{c}]" for c in black_stones)
    white_stones_str = "AW" + "".join(f"[{c}]" for c in white_stones)
    start_player = problem.get("Start", "B")
    rank = problem.get("Comments", "")

    # Start with stones and comments
    root = f"(;{black_stones_str}{white_stones_str}{get_comments(key, rank)}"
    # Add solution variations
    root += variations_to_sgf(merge_variations(all_solutions), start_player)

    return root + ")"


def convert_go_problems_to_sgf(data) -> str:
    header = "GM[1]FF[4]SZ[19]"
    sgf = []
    for key, problem in data.items():
        sgf.append(generate_sgf_node(key, problem))
    return "(;" + header + "\n".join(sgf) + ")"


def main() -> None:
    with open(input_file, "r") as f:
        jsonProblems = json.load(f)
    print(f"Loaded {len(jsonProblems)} problems from {input_file}")
    # print(f"Example: {jsonProblems["Problem 1"]}")
    sgf_output = convert_go_problems_to_sgf(jsonProblems)
    # print(sgf_output)

    output_file = f"{output_folder}/{BOOK.split("/")[-1]}.sgf"
    print(f"Saving output to '{output_file}'")
    with open(f"{output_folder}/{BOOK.split("/")[-1]}.sgf", "w") as f:
        f.write(sgf_output)


if __name__ == "__main__":
    main()
