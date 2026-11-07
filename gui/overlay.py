from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QTextEdit
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter
from PySide6 import QtGui, QtCore

import csv


class Overlay(QWidget):
    change_ui = Signal(dict, name="change_ui")
    
    def __init__(self):
        super().__init__()
        self.companies = []
        self.clear_flag = 0
        self.first_paint = 1 # Flag to prevent rectangles on initialization paintEvent
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

    # Data dictionary contains block_num, conf, height, left, level, line_num, page_num, par_num, text, top, width
    # and block num
    def highlight_area(self, data):
        #self.stuff.setText(json.dumps(text)) # Note to self: remove placeholder and implement actual highlighting mechanics
        with open("companies.csv", "rt") as f:
            row = 0
            reader = csv.reader(f)
            for line in reader:
                if line[0] != "":
                    self.companies.append(line[0])
                    row += 1
            f.close()
        self.screen_data = data
        self.first_paint = 0
        self.repaint()

    def paintEvent(self, event:QtGui.QPaintEvent):
        if not self.first_paint and not self.clear_flag:
            self.painter = QPainter()
            self.painter.begin(self)
            for i in range(len(self.screen_data["text"])):
                for company in self.companies:
                    words = company.split()
                    if len(words) <= 1 and str.lower(self.screen_data["text"][i]) == str.lower(company):
                        rect = QtCore.QRect(self.screen_data["left"][i], self.screen_data["top"][i], self.screen_data["width"][i], self.screen_data["height"][i])
                        self.painter.fillRect(rect, Qt.GlobalColor.yellow)
                        self.painter.drawRect(rect)
                    elif len(words) > 1:
                        for word in words:
                            if str.lower(self.screen_data["text"][i]) == str.lower(word):
                                rect = QtCore.QRect(self.screen_data["left"][i], self.screen_data["top"][i], self.screen_data["width"][i], self.screen_data["height"][i])
                                self.painter.fillRect(rect, Qt.GlobalColor.yellow)
                                self.painter.drawRect(rect)
            """for company in self.companies:
                words = company.split()
                for word in words:
                    for i in range(len(self.screen_data["text"])):
                        if len(words) <= 1 and str.lower(self.screen_data["text"][i]) == str.lower(word):
                            rect = QtCore.QRect(self.screen_data["left"][i], self.screen_data["top"][i], self.screen_data["width"][i], self.screen_data["height"][i])
                            self.painter.fillRect(rect, Qt.GlobalColor.yellow)
                            self.painter.drawRect(rect)
                        elif len(words) > 1:
                            if str.lower(self.screen_data["text"][i]) == str.lower(word):
                                rect = QtCore.QRect(self.screen_data["left"][i], self.screen_data["top"][i], self.screen_data["width"][i], self.screen_data["height"][i])
                                rects.append(rect)
                            else:
                                rects.clear()
                                break
                for rect in rects:
                    self.painter.fillRect(rect, Qt.GlobalColor.yellow)
                    self.painter.drawRect(rect)"""
            self.painter.end()
            
        self.clear_flag = 0
        return super().paintEvent(event)