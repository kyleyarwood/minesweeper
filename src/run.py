from app import App
from PyQt5.QtWidgets import *
from sys import argv, exit
from json import load

def get_hi_scores():
    with open('hi_scores.json', 'r') as f:
        return load(f)

def main():
    hi_scores = get_hi_scores()
    print(hi_scores)
    try:
        rows, cols, num_mines = int(argv[1]), int(argv[2]), int(argv[3])
    except:
        rows = cols = 8
        num_mines = 10
    app = QApplication(argv)
    ex = App(rows=rows, cols=cols, num_mines=num_mines, hi_scores=hi_scores)
    app.exec_()
    
    

if __name__ == "__main__":
    main()

