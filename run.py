from board import Board
from app import App
from PyQt5.QtWidgets import *
from sys import argv, exit

def main():
	"""board = Board(rows=8, cols=8, num_mines=10)	
	#board.click(0, 0)
	print(board)
	while not board.is_solved():
		i, j = map(int, input('enter coords').split())
		if not board.click(i, j):
			print("you screwed up")
			break
		print(board)"""
	app = QApplication(argv)
	ex = App(rows=8, cols=8)
	exit(app.exec_())


if __name__ == "__main__":
	main()
