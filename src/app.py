from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor, QIcon, QPixmap
from board import Board
from json import dumps

class App(QWidget):
    def __init__(self, rows, cols, num_mines, hi_scores):
        self.WINDOW_BAR_HEIGHT = 23
        self.WINDOW_WIDTH = 8
        super().__init__()
        self.game_over = False
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.hi_scores = hi_scores
        self.title = 'Minesweeper'
        self.left = 0
        self.top = 0
        self.width = 1440
        self.height = 720
        self.board_labels = []
        self.board = None
        self.window = QWidget(self)
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height+30)
        self.window.setFocus()
        self.window.setLayout(self.init_layout())
        self.show()

    def init_layout(self):
        self.board = Board(rows=self.rows, cols=self.cols, num_mines=self.num_mines)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        for i in range(self.rows):
            hlayout = QHBoxLayout()
            hlayout.setSpacing(0)
            board_row = []
            for j in range(self.cols):
                label = QLabel(self)
                pixmap = QPixmap('../img/facingDown.png')
                sf = self._scaling_factor()
                pixmap = pixmap.scaledToWidth(sf).scaledToHeight(sf)
                label.setPixmap(pixmap)
                hlayout.addWidget(label)
                board_row.append(label)
            layout.addLayout(hlayout)
            self.board_labels.append(board_row)
        
        layout.addWidget(self.restart_button())
        layout.setContentsMargins(0, 0, 0, 0)
        self.updateUI()
        self.game_over = False
        return layout

    def restart_board(self):
        self.board = Board(rows=self.rows, cols=self.cols, num_mines=self.num_mines)
        self.game_over = False
        self.updateUI()

    def restart_button(self):
        button = QPushButton('Restart', self)
        button.clicked.connect(self.restart_board)
        return button

    def _get_pixmap(self, cell: str = 'E') -> QPixmap:
        pixmap = None
        if cell == 'E' or cell == 'M':
            pixmap = QPixmap('../img/facingDown.png')
        elif cell in map(str, range(9)):
            pixmap = QPixmap('../img/' + cell + '.png')
        elif cell == 'F':
            pixmap = QPixmap('../img/flagged.png')
        else:
            pixmap = QPixmap('../img/facingDown.png')
        sf = self._scaling_factor()
        pixmap = pixmap.scaledToWidth(sf).scaledToHeight(sf)
        return pixmap

    def _scaling_factor(self):
        return min(self.width, self.height)//max(self.rows, self.cols)

    def mouseReleaseEvent(self, event):
        if self.game_over:
            return
        x, y = self._get_hovering_cell(QCursor.pos(), self.pos())
        if not self.board.in_bounds(y, x):
            return
        if event.button() == 1:
            if not self.board.click(y, x):
                self.game_over = True
                self.display_game_over()
        else:
            self.board.flag(y, x)
        self.updateUI()
        if self.board.is_solved():
            self.game_over = True
            self.board.end_game()
            self.display_win()

    def _get_hovering_cell(self, cursor_pos, window_pos):
        sf = self._scaling_factor()
        return (cursor_pos.x() - self.WINDOW_WIDTH - window_pos.x())//sf, (cursor_pos.y() - self.WINDOW_BAR_HEIGHT - window_pos.y())//sf

    def keyPressEvent(self, event):
        if self.game_over:
            return
        x, y = self._get_hovering_cell(QCursor.pos(), self.pos())
        if not self.board.in_bounds(y, x):
            return
        if event.key() == 32:
            cell = (str(self.board).split('\n'))[y][x]
            if cell in ('E', 'M', 'F'):
                self.board.flag(y, x)
            elif cell in map(str, range(9)) and self.board.all_flagged(y, x):
                if not self.board.clear(y, x):
                    self.game_over = True
                    self.display_game_over()
        self.updateUI()
        if self.board.is_solved():
            self.board.end_game()
            self.game_over = True
            self.display_win()

    def display_win(self):
        t = round(self.board.total_time(), 2)
        win_alert = QMessageBox(self.window)
        win_alert.setText("You've won! " + str(t))
        if (str((self.rows, self.cols, self.num_mines)) not in self.hi_scores or
            self.hi_scores[str((self.rows, self.cols, self.num_mines))] > t):
            self.hi_scores[str((self.rows, self.cols, self.num_mines))] = t
            self.write_hi_scores()
            win_alert.setText("You've won! NEW HI SCORE! " + str(t))
        win_alert.exec_()

    def write_hi_scores(self):
        with open('hi_scores.json', 'w') as f:
            f.write(dumps(self.hi_scores))

    def display_game_over(self):
        game_over_alert = QMessageBox(self.window)
        game_over_alert.setText("You've lost!")
        game_over_alert.exec_()

    def updateUI(self) -> None:
        board_encoding = str(self.board)
        for i, board_row in enumerate(board_encoding.split('\n')):
            for j, cell in enumerate(board_row):
                self.board_labels[i][j].setPixmap(self._get_pixmap(cell))
                self.board_labels[i][j].repaint()
