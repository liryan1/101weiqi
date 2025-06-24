from typing import List, Tuple
from copy import deepcopy

EMPTY = "."
BLACK = "b"
WHITE = "w"

Coordinate = Tuple[int, int]
Board = List[List[str]]

def is_outside(coord: Coordinate, size: int) -> bool:
  y, x = coord[0], coord[1]
  return not (0 <= y < size and 0 <= x < size)

def get_neighbors(coord: Coordinate) -> List[Coordinate]:
  y, x = coord[0], coord[1]
  neighbors: List[Coordinate] = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
  return neighbors

def get_status(board: Board, coord: Coordinate) -> str:
  y, x = coord[0], coord[1]
  return board[y][x]

def remove_stones(board: Board, group: List[Coordinate]) -> Board:
  for y, x in group:
    board[y][x] = EMPTY
  return board

def get_dead_group(board: Board, coord: Coordinate, color: str) -> List[Coordinate]:
  if is_outside(coord, len(board)):
    return []
  y, x = coord
  if color == EMPTY or board[y][x] != color:
    return []
  opponent = WHITE if color == BLACK else BLACK
  new_board = deepcopy(board)
  dead_group = []
  stack = [coord]
  while stack:
    coord = stack.pop()
    if is_outside(coord, len(board)):
      continue
    y, x = coord[0], coord[1]
    if new_board[y][x] == color:
      new_board[y][x] = opponent
      dead_group.append((y, x))
      stack += get_neighbors((y, x))
    elif new_board[y][x] == opponent:
      continue
    else:
      return []
  return dead_group

def handle_move(board: Board, cur_move: Coordinate, color: str) -> Tuple[Board, Coordinate | None]:
  ko_spot = None
  y, x = cur_move
  if is_outside(cur_move, len(board)) or board[y][x] != EMPTY:
    return (board, ko_spot)
  opponent = WHITE if color == BLACK else BLACK
  new_board = deepcopy(board)
  neighbors = get_neighbors(cur_move)
  new_board[y][x] = color
  killed = []
  for (y, x) in neighbors:
    killed += get_dead_group(new_board, (y, x), opponent)
  suicide = get_dead_group(new_board, cur_move, color)
  if len(killed) == 0 and len(suicide) > 0:
    return (board, ko_spot)
  if len(killed) == 1 and len(suicide) == 1:
    ko_spot = killed[0]
  new_board = remove_stones(new_board, killed)
  return (new_board, ko_spot)





