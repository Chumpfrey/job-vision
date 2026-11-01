import sys

from PySide6 import QtWidgets
from gui.widgets import MainWindow

class MyApplication():
    def __init__(self):
        app = QtWidgets.QApplication([])
        
        menu = MainWindow()
        menu.resize(800, 800)
        menu.show()
      
        sys.exit(app.exec())