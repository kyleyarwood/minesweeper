from cell import Cell
from random import choice
from typing import List, Tuple, Set
from time import time

class Board:
    def __init__(self, rows: int, cols: int, num_mines: int):
        self._first_click = True
        self._board = [[Cell.EMPTY for col in range(cols)] 
                                    for row in range(rows)]
        self._start_time = None
        self._end_time = None
        self._num_mines = num_mines
        self._flags_left = num_mines

    def end_game(self):
        self._end_time = time()

    def get_start_time(self):
        return self._start_time

    def is_first_click(self) -> bool:
        return self._first_click

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < len(self._board) and 0 <= col < len(self._board[row])

    def all_flagged(self, row: int, col: int) -> bool:
        num_flags_needed = self._board[row][col].value
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if not self.in_bounds(i, j):
                    continue
                if self._board[i][j] in (Cell.EMPTY_FLAGGED, Cell.MINE_FLAGGED):
                    num_flags_needed -= 1
        return num_flags_needed == 0

    def clear(self, row: int, col: int) -> bool:
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if not self.in_bounds(i, j):
                    continue
                if self._board[i][j] in (Cell.EMPTY, Cell.MINE):
                    if not self.click(i, j):
                        return False
        return True

    def total_time(self):
        return self._end_time - self._start_time

    def click(self, row: int, col: int) -> bool:
        if self._first_click:
            self._start_time = time()
            self._first_click = False
            self._generate_board(row, col)
        visited = set()
        clicked_mine = self._dfs(row, col, visited)
        return clicked_mine

    def get_flags_left(self) -> int:
        return self._flags_left

    def flag(self, row: int, col: int) -> None:
        if self._board[row][col] == Cell.EMPTY:
            self._board[row][col] = Cell.EMPTY_FLAGGED
            self._flags_left -= 1
        elif self._board[row][col] == Cell.EMPTY_FLAGGED:
            self._board[row][col] = Cell.EMPTY
            self._flags_left += 1
        elif self._board[row][col] == Cell.MINE:
            self._board[row][col] = Cell.MINE_FLAGGED
            self._flags_left -= 1
        elif self._board[row][col] == Cell.MINE_FLAGGED:
            self._board[row][col] = Cell.MINE
            self._flags_left += 1

    def is_solved(self):
        return all(all(c not in (Cell.EMPTY, Cell.EMPTY_FLAGGED) for c in row) for row in self._board)

    def _dfs(self, row: int, col: int, visited: Set) -> bool:
        if self._board[row][col] == Cell.MINE:
            return False
        elif self._board[row][col] != Cell.EMPTY:
            return True
        
        self._set_mines_surrounding(row, col)
        if self._board[row][col] != Cell.ZERO:
            return True
        visited.add((row, col))
        for neighbour in self._get_neighbours(row, col):
            if neighbour not in visited:
                self._dfs(neighbour[0], neighbour[1], visited)
        return True

    def _set_mines_surrounding(self, row: int, col: int) -> None:
        num_mines_surrounding = self._get_num_mines_surrounding(row, col)
        self._board[row][col] = Cell(num_mines_surrounding)

    def _get_neighbours(self, row: int, col: int) -> List[Tuple[int, int]]:
        neighbours = []
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if (0 <= i < len(self._board) 
                    and 0 <= j < len(self._board[i]) 
                    and (i != row or j != col)):
                    neighbours.append((i, j))
        return neighbours

    def _generate_board(self, row: int, col: int) -> None:
        options = set([(i, j) for i in range(len(self._board)) for j in range(len(self._board[0]))])
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if (i, j) in options:
                    options.remove((i, j))
        for i in range(self._num_mines):
            mine = choice(tuple(options))
            options.remove(mine)
            self._board[mine[0]][mine[1]] = Cell.MINE

    def board_3bv(self) -> int:
        cells_with_zero_mines = self._get_cells_with_zero_mines()
        result = self._get_num_empty_cell_islands(cells_with_zero_mines)
        for i, row in enumerate(self._board):
            for j, cell in enumerate(row):
                if cell not in (Cell.MINE, Cell.MINE_FLAGGED) and \
                    set(self._get_neighbours(i, j)).intersection(cells_with_zero_mines) == set():
                    result += 1
        return result

    def _get_cells_with_zero_mines(self) -> Set:
        cells_with_zero_mines = set()
        for i, row in enumerate(self._board):
            for j in range(len(row)):
                if self._get_num_mines_surrounding(i, j) == 0:
                    cells_with_zero_mines.add((i, j))
        return cells_with_zero_mines

    def _get_num_empty_cell_islands(self, cells_with_zero_mines: Set) -> int:
        visited = set()
        result = 0
        for i, row in enumerate(self._board):
            for j, cell in enumerate(row):
                if (i, j) not in visited and \
                    (i, j) in cells_with_zero_mines:
                    self._traverse_empty_cell_island(i, j, visited, cells_with_zero_mines)
                    result += 1
        return result

    def _traverse_empty_cell_island(self, row: int, col: int, visited: Set, cells_with_zero_mines: Set):
        visited.add((row, col))
        for x, y in self._get_neighbours(row, col):
            if (x, y) not in visited and (x, y) in cells_with_zero_mines:
                self._traverse_empty_cell_island(x, y, visited, cells_with_zero_mines)

    def _get_num_mines_surrounding(self, row: int, col: int) -> int:
        return self._get_num_cells_of_types_surrounding(row, col, [Cell.MINE, Cell.MINE_FLAGGED])

    def _get_num_cells_of_types_surrounding(self, row: int, col: int, types: List[Cell]) -> int:
        num_cells_of_types_surrounding = 0
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if (0 <= i < len(self._board) and
                    0 <= j < len(self._board[i]) and
                    self._board[i][j] in types):
                    num_cells_of_types_surrounding += 1
        return num_cells_of_types_surrounding

    def __str__(self):
        result = []
        for row in self._board:
            for col in row:
                if 0 <= col.value < 9:
                    result.append(str(col.value))
                elif col == Cell.EMPTY:
                    result.append("E")
                elif col == Cell.MINE:
                    result.append("M")
                else:
                    result.append("F")
            result.append("\n")
        return ''.join(result)[:-1]
