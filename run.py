from board import Board
from app import App
from PyQt5.QtWidgets import *
from sys import argv, exit

def main():
	rows, cols, num_mines = int(argv[1]), int(argv[2]), int(argv[3])
	app = QApplication(argv)
	board = Board(rows=rows, cols=cols, num_mines=num_mines)
	ex = App(rows=rows, cols=cols, board=board)
	#board.click(0, 0)
	print(str(board))
	ex.updateUI()
	app.exec_()
	

if __name__ == "__main__":
	main()

