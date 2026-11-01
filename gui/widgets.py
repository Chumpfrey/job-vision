import random
from PySide6 import QtCore, QtWidgets


class CSVWidget(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__(10, 1)

        self.setColumnWidth(0, 200)
        self.cellChanged.connect(self.expand_row)
        self.cellChanged.connect(self.select_next_row)
    
    def expand_row(self):
        if (self.item(self.rowCount() - 1, 0) is not None):
            self.setRowCount(self.rowCount() + 1)
    
    def select_next_row(self):
        self.setCurrentCell(self.currentRow() + 1, 0)
    
    
class CSVView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        vertical_layout = QtWidgets.QVBoxLayout()
        
        horizontal_layout_widget = QtWidgets.QWidget()
        horizontal_layout = QtWidgets.QHBoxLayout()
        import_button = QtWidgets.QPushButton("Import")
        export_button = QtWidgets.QPushButton("Export")
        horizontal_layout.addWidget(import_button)
        horizontal_layout.addWidget(export_button)
        horizontal_layout_widget.setLayout(horizontal_layout)
        
        vertical_layout.addWidget(horizontal_layout_widget)
        vertical_layout.addWidget(CSVWidget())
        self.setLayout(vertical_layout)
            

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.hello = ["Hello World", "Goodbye", "Nope"]
        
        self.button = QtWidgets.QPushButton("Click")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)
    
    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))
        
        
class CentralWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        
        self.addTab(MyWidget(), "Test")
        self.addTab(CSVView(), "Companies")
        

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setCentralWidget(CentralWidget())
    
        