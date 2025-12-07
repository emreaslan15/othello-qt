from PyQt6.QtWidgets import *
import sys
from OthelloCLI import Othello 

class GridCell(QPushButton):
    def __init__(self, x, y, gui):
        super().__init__()
    
        self.x = x
        self.y = y
        self.setText(x + y)
        self.setFixedSize(50, 50)
        self.gui = gui

        self.update()
        self.clicked.connect(self.on_click)
    '''
    def on_click(self):
        ox = ord(self.x) - ord('A')
        oy = int(self.y) - 1

        if self.gui.o.move(ox, oy):
            self.gui.update_from_board()
        else:
            print("Illegal move")
    '''

    def on_click(self):
        ox = ord(self.x) - ord('A')
        oy = int(self.y) - 1

        # Attempt the move
        if self.gui.o.move(ox, oy):
            # Update board display
            self.gui.update_from_board()

            # After move: check if opponent must pass
            if not self.gui.o.can_move() and not self.gui.o.game_over():
                self.gui.o.skip()
                self.gui.update_from_board()
                self.gui.update_status("No legal moves — passing turn")
            else:
                self.gui.update_status()
        else:
            # Illegal move
            self.gui.update_status("Illegal move")

    def update(self):
        ox = ord(self.x) - ord('A')
        oy = int(self.y) - 1
        val = self.gui.o.board[ox][oy]

        if val == 0:
            self.setStyleSheet("background-color: green; color: white;")
        elif val == 1:
            self.setStyleSheet("background-color: white; color: black;")
        elif val == -1:
            self.setStyleSheet("background-color: black; color: white;")

class OthelloGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.o = Othello()
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.setWindowTitle("Othello | Reversi")

        layout = QGridLayout()
        self.grid = []

        for i in range(8):
            row = []
            for j in range(8):
                btn = GridCell(chr(j + ord('A')), str(i + 1), self)
                layout.addWidget(btn, i, j)
                row.append(btn)
            self.grid.append(row)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.update_from_board()

    def update_from_board(self):
        for i in range(8):
            for j in range(8):
                self.grid[i][j].update()
        self.update_status()

    def update_status(self, message=None):
        black = self.o.score(self.o.BLACK)
        white = self.o.score(self.o.WHITE)
        turn = self.o.player_name()

        if message is None:
            self.status.showMessage(f"Turn: {turn} | Black: {black}  White: {white}")
        else:
            self.status.showMessage(f"{message} — Turn: {turn} | Black: {black}  White: {white}", 3000)

app = QApplication(sys.argv)
window = OthelloGUI()
window.show()
app.exec()
