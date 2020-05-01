from app import App
from PyQt5.QtWidgets import *
from sys import argv, exit
from json import load

def get_stats():
    with open('stats.json', 'r') as f:
        return load(f)

def main():
    stats = get_stats()
    try:
        rows, cols, num_mines = int(argv[1]), int(argv[2]), int(argv[3])
    except:
        rows = cols = 8
        num_mines = 10
    app = QApplication(argv)
    ex = App(rows=rows, cols=cols, num_mines=num_mines, stats=stats)
    app.exec_()
    
    

if __name__ == "__main__":
    main()

