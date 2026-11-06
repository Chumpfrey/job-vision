from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QTextEdit
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, Qt

import json


class Overlay(QWidget):
    change_ui = Signal(dict, name="change_ui")
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Overlay")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet('background-color: transparent;')
        
        self.stuff = QTextEdit()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.stuff)
        self.setLayout(layout)
        self.resize(1920, 1080) # Note to self: change hard-coded resolution to dynamic resolution
        self.show()

    def highlight_area(self, text):
        self.stuff.setText(json.dumps(text)) # Note to self: remove placeholder and implement actual highlighting mechanics