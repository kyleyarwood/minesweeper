from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from board import Board

class App(QWidget):
	def __init__(self, rows, cols, board):
		self.WINDOW_BAR_HEIGHT = 23
		super().__init__()
		self.rows = rows
		self.cols = cols
		self.title = 'Minesweeper'
		self.left = 10
		self.top = 10
		self.width = 1080
		self.height = 720
		self.board_labels = []
		self.board = board
		self.window = QWidget(self)
		self.initUI()

	def initUI(self) -> None:
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		layout = QVBoxLayout()
		layout.setSpacing(0)
		for i in range(self.rows):
			hlayout = QHBoxLayout()
			hlayout.setSpacing(0)
			board_row = []
			for j in range(self.cols):
				label = QLabel(self)
				pixmap = QPixmap('img/facingDown.png')
				sf = self._scaling_factor()
				pixmap = pixmap.scaledToWidth(sf).scaledToHeight(sf)
				label.setPixmap(pixmap)
				label.mousePressEvent = self.click_event
				hlayout.addWidget(label)
				board_row.append(label)
			layout.addLayout(hlayout)
			self.board_labels.append(board_row)

		layout.setContentsMargins(0, 0, 0, 0)
		self.window.setFocus()
		self.window.setLayout(layout)
		self.show()

	def _get_pixmap(self, cell: str = 'E') -> QPixmap:
		pixmap = None
		if cell == 'E' or cell == 'M':
			pixmap = QPixmap('img/facingDown.png')
		elif cell in map(str, range(9)):
			pixmap = QPixmap('img/' + cell + '.png')
		elif cell == 'F':
			pixmap = QPixmap('img/flagged.png')
		else:
			pixmap = QPixmap('img/facingDown.png')
		sf = self._scaling_factor()
		pixmap = pixmap.scaledToWidth(sf).scaledToHeight(sf)
		return pixmap

	def _scaling_factor(self):
		return min(self.width, self.height)//max(self.rows, self.cols)

	def click_event(self, event):
		cursor_pos = QCursor.pos()
		window_pos = self.pos()
		sf = self._scaling_factor()
		x, y = (cursor_pos.x() - window_pos.x())//sf, (cursor_pos.y() - self.WINDOW_BAR_HEIGHT - window_pos.y())//sf
		#x = y = 0
		#print(event.button())
		if event.button() == 1:
			self.board.click(y, x)
		else:
			self.board.flag(y, x)
		self.updateUI()
		if self.board.is_solved():
			print("You've won!")

	def updateUI(self) -> None:
		board_encoding = str(self.board)
		for i, board_row in enumerate(board_encoding.split('\n')):
			for j, cell in enumerate(board_row):
				self.board_labels[i][j].setPixmap(self._get_pixmap(cell))
