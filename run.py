from board import Board
from app import App
from PyQt5.QtWidgets import *
from sys import argv, exit

def main():
	try:
		rows, cols, num_mines = int(argv[1]), int(argv[2]), int(argv[3])
	except:
		rows = cols = 8
		num_mines = 10
	app = QApplication(argv)
	board = Board(rows=rows, cols=cols, num_mines=num_mines)
	ex = App(rows=rows, cols=cols, num_mines=num_mines, board=board)
	app.exec_()
	

if __name__ == "__main__":
	main()

