from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QTextEdit
from PySide6 import QtWidgets
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter
from PySide6 import QtGui, QtCore

import csv, os.path


class Overlay(QWidget):
    change_ui = Signal(dict, name="change_ui")
    
    def __init__(self):
        super().__init__()
        self.companies = []
        self.clear_flag = 0
        self.first_paint = 1 # Flag to prevent rectangles on initialization paintEvent
        self.setWindowTitle("Overlay")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet('background-color: transparent; border: none;')
        
        self.stuff = QTextEdit()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.stuff)
        self.setLayout(layout)
        height = self.screen().size().height()
        width = self.screen().size().width()
        self.resize(width, height) # Note to self: change hard-coded resolution to dynamic resolution
        self.show()

    # Data dictionary contains block_num, conf, height, left, level, line_num, page_num, par_num, text, top, width
    # and block num
    def highlight_area(self, data):
        filename = "companies.csv"
        if os.path.isfile(filename):
            with open(filename, "rt") as f:
                row = 0
                reader = csv.reader(f)
                for line in reader:
                    if line[0] != "":
                        self.companies.append(line[0])
                        row += 1
                f.close()
            
            self.screen_data = {
                "block_num": [],
                "conf": [],
                "height": [],
                "left": [],
                "level": [],
                "line_num": [],
                "page_num": [],
                "par_num": [],
                "text": [],
                "top": [],
                "width": []                       
            }
            
            # Clears out all empty strings
            for i in range(len(data["text"])):
                if data["text"][i].replace(" ", "") != "":
                    self.screen_data["block_num"].append(data["block_num"][i])
                    self.screen_data["conf"].append(data["conf"][i])
                    self.screen_data["height"].append(data["height"][i])
                    self.screen_data["left"].append(data["left"][i])
                    self.screen_data["level"].append(data["level"][i])
                    self.screen_data["line_num"].append(data["line_num"][i])
                    self.screen_data["page_num"].append(data["page_num"][i])
                    self.screen_data["par_num"].append(data["par_num"][i])
                    self.screen_data["text"].append(data["text"][i])
                    self.screen_data["top"].append(data["top"][i])
                    self.screen_data["width"].append(data["width"][i])
                    
            self.first_paint = 0
            self.repaint()

    def paintEvent(self, event:QtGui.QPaintEvent):
        highlight = QtGui.QColor(50, 125, 255, 70)
        if not self.first_paint and not self.clear_flag:
            self.painter = QPainter()
            self.painter.begin(self)
            connected_rects = []
            for company in self.companies:
                for i in range(len(self.screen_data["text"])):
                    words = company.split()
                    
                    # Processes company names that are a single word
                    if len(words) <= 1 and str.lower(self.screen_data["text"][i]) == str.lower(company):
                        rect = QtCore.QRect(self.screen_data["left"][i], self.screen_data["top"][i], self.screen_data["width"][i], self.screen_data["height"][i])
                        self.painter.fillRect(rect, highlight)
                        self.painter.fillRect
                        self.painter.drawRect(rect)
                        
                    # Processes company names that are multiple words
                    elif len(words) > 1:
                        for j in range(len(words)):
                            # Take note of words that might be a part of a company name
                            if str.lower(self.screen_data["text"][i]) == str.lower(words[j]):
                                rect = QtCore.QRect(self.screen_data["left"][i], self.screen_data["top"][i], self.screen_data["width"][i], self.screen_data["height"][i])
                                connected_rects.append(rect)
                                break
                            
                            # If found company names don't match table, throw highlight sequence away
                            if j == len(words) - 1 and words[j] != words[len(words) - 1]:
                                connected_rects.clear()

                        if len(words) == len(connected_rects):
                            prev_rect = QtCore.QRect(0, 0, 0, 0)
                            for rect in connected_rects:
                                self.painter.fillRect(rect, highlight)
                                self.painter.drawRect(rect)
                            connected_rects.clear()    
                            
            self.painter.end()
            
        self.clear_flag = 0
        return super().paintEvent(event)