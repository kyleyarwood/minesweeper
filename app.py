from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap

class App(QWidget):
	def __init__(self, rows, cols):
		super().__init__()
		self.rows = rows
		self.cols = cols
		self.title = 'Minesweeper'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.window = QWidget(self)
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		layout = QVBoxLayout()
		layout.setSpacing(0)
		for i in range(self.rows):
			hlayout = QHBoxLayout()
			hlayout.setSpacing(0)
			for j in range(self.cols):
				label = QLabel(self)
				pixmap = QPixmap('img/facingDown.png')
				scaling_factor = min(self.width, self.height)//max(self.rows, self.cols)
				pixmap = pixmap.scaledToWidth(scaling_factor).scaledToHeight(scaling_factor)
				label.setPixmap(pixmap)
				#label.setFixedSize(10,10)
				hlayout.addWidget(label)
			layout.addLayout(hlayout)
		#self.resize(pixmap.width(), pixmap.height())
		self.window.setFocus()
		self.window.setLayout(layout)
		self.show()
