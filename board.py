from cell import Cell
from random import choice
from typing import List, Tuple, Set
from time import time

class Board:
	def __init__(self, rows: int, cols: int, num_mines: int):
		self._first_click = True
		self._board = [[Cell.EMPTY for row in range(rows)] 
									for col in range(cols)]
		self._num_mines = num_mines

	def click(self, row: int, col: int) -> bool:
		if self._first_click:
			start = time()
			self._first_click = False
			self._generate_board(row, col)
		visited = set()
		clicked_mine = self._dfs(row, col, visited)
		if self.is_solved():
			end = time()
		return clicked_mine

	def flag(self, row: int, col: int) -> None:
		if self._board[row][col] == Cell.EMPTY:
			self._board[row][col] = Cell.EMPTY_FLAGGED
		elif self._board[row][col] == Cell.EMPTY_FLAGGED:
			self._board[row][col] = Cell.EMPTY
		elif self._board[row][col] == Cell.MINE:
			self._board[row][col] = Cell.MINE_FLAGGED
		elif self._board[row][col] == Cell.MINE_FLAGGED:
			self._board[row][col] = Cell.MINE

	def is_solved(self):
		return all(all(c != Cell.EMPTY for c in row) for row in self._board)

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
		num_mines_surrounding = 0
		for i in range(row-1, row+2):
			for j in range(col-1, col+2):
				if (0 <= i < len(self._board) and
					0 <= j < len(self._board[i]) and
					self._board[i][j] in (Cell.MINE, Cell.MINE_FLAGGED)):
					num_mines_surrounding += 1
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

	def get_board(self):
		return self._board

	def __str__(self):
		s = ""
		for row in self._board:
			for col in row:
				if 0 <= col.value < 9:
					s += str(col.value)
				elif col == Cell.EMPTY:
					s += "E"
				elif col == Cell.MINE:
					s += "M"
				else:
					s += "F"
			s += "\n"
		return s[:-1]
