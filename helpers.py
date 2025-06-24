from go import get_empty_board, convert_coordinate, Go_game, EMPTY, BLACK, WHITE


def flip(s: str):
    x, y = s[0], s[1]
    return chr(19 - (ord(y) - 96) + 97) + chr(19 - (ord(x) - 96) + 97)


def to_lower_left(black, white):
    new_black, new_white = black, white

    left = 0
    right = 0
    top = 0
    bottom = 0

    for x, y in black + white:
        if x < "j":
            left += 1
        elif x > "j":
            right += 1
        if y < "j":
            top += 1
        elif y > "j":
            bottom += 1
    
    if right > left:
        new_black = [chr(19 - (ord(b[0]) - 96) + 97) + b[1] for b in new_black]
        new_white = [chr(19 - (ord(b[0]) - 96) + 97) + b[1] for b in new_white]

    if top > bottom:
        new_black = [b[0] + chr(19 - (ord(b[1]) - 96) + 97) for b in new_black]
        new_white = [b[0] + chr(19 - (ord(b[1]) - 96) + 97) for b in new_white]
    
    return (new_black, new_white)


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
        new_board = go.play_move((y, x))
        if new_board == board:
            return max_distance
        board = new_board
        cy, cx = move[0], move[1]
        for sy, sx in black:
            distance += (ord(cx) - ord(sx)) + (ord(cy) - ord(sy))
        for sy, sx in white:
            distance += (ord(cx) - ord(sx)) + (ord(cy) - ord(sy))

    return abs(distance)
