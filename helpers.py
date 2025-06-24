from go import *

def flip(s: str):
    x, y = s[0], s[1]
    return chr(19 - (ord(y) - 96) + 97) + chr(19 - (ord(x) - 96) + 97)


def to_lower_left(coords: list[str], size: int) -> list[str]:
    return [
        chr(size - (ord(b[0]) - 96) + 97) + chr(size - (ord(b[1]) - 96) + 97)
        for b in coords
    ]


def is_in_lower_left(stones: list[str]) -> bool:
    count = 0
    for x, y in stones:
        if x <= "j" <= y:
            count += 1
    return count >= len(stones) / 2


def make_fat(stones: list[str]):
    """Make the stones fat"""
    return [flip(stone) for stone in stones]


def is_fat(stones):
    """Check if there are more stones horizontally than vertically"""
    fat = "a"
    tall = "s"
    for x, y in stones:
        fat = max(fat, x)
        tall = min(tall, y)
    return ord(fat) + ord(tall) > 211


def get_solution_distance(black: list[str], white: list[str], solution: list[str]):
    board = get_empty_board(19)
    for coord in black:
        x, y = convert_coordinate(coord)
        board[y][x] = BLACK

    for coord in white:
        x, y = convert_coordinate(coord)
        board[y][x] = WHITE

    go = Go_game(19, board)

    distance = 0
    max_distance = 10 ** 8
    for move in solution:
        [x, y] = convert_coordinate(move)
        new_board = go.play_move([y, x])
        if new_board == board:
            return max_distance
        board = new_board
        cy, cx = move[0], move[1]
        for sy, sx in black:
            distance += (ord(cx) - ord(sx)) + (ord(cy) - ord(sy))
        for sy, sx in white:
            distance += (ord(cx) - ord(sx)) + (ord(cy) - ord(sy))
    
    return abs(distance)


