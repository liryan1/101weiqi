from go_logic import *
from typing import List, Tuple

Coordinate = Tuple[int, int]
Board = List[List[str]]
State = Tuple[Board, str]

def get_empty_board(size: int) -> Board:
  board = [[EMPTY] * size for _ in range(size)]
  return board


def is_legal_board(board: Board) -> int:
  p = [EMPTY, BLACK, WHITE]
  for i in range(len(board)):
    for j in range(len(board)):
      color = board[i][j]
      if color not in p:
        return -1
      dead_group = get_dead_group(board, (i, j), color)
      if dead_group:
        return -2
  return 1


def convert_coordinate(string_coord: str) -> Coordinate:
  [x, y] = string_coord
  return [ord(x) - 97, ord(y) - 97]



class Go_game:

  def __init__(self, size: int, board: Board | None = None, color: str = BLACK) -> None:

    if color != BLACK and color != WHITE:
      raise(ValueError("invalid color"))


    self.board: Board = board if board else get_empty_board(size)
    self.size = size
    is_legal = is_legal_board(self.board)
    if is_legal < 0:
      if is_legal == -1:
        raise(ValueError("invalid character exist"))
      else:
        raise(ValueError("Dead group exist"))
    self.color: str = color


  def _change_color(self):
    self.color = WHITE if self.color == BLACK else BLACK


  def play_move(self, move: Coordinate) -> Board:
    new_board, new_ko_spot = handle_move(self.board, move, self.color)
    if self.board == new_board:
      return self.board
    self.board = new_board
    self._change_color()
    return new_board
  



  
