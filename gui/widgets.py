import csv
import random
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog, QMessageBox, QPushButton, QWidget


class CSVWidget(QtWidgets.QTableWidget):
    def __init__(self):
        try: 
            super().__init__(1, 1)
            with open("companies.csv", "rt") as f:
                row = 0
                reader = csv.reader(f)
            
                for line in reader:
                    item = QtWidgets.QTableWidgetItem(line[0])
                    self.setItem(row, 0, item)
                    row += 1
                    self.expand_row()
        except:
            super().__init__(10, 1)
            
        self.setColumnWidth(0, 200)
        self.cellChanged.connect(self.expand_row)
        self.cellChanged.connect(self.select_next_row)
        self.cellChanged.connect(self.save_progress)
    
    def expand_row(self):
        if (self.item(self.rowCount() - 1, 0) is not None):
            self.setRowCount(self.rowCount() + 1)
    
    def select_next_row(self):
        self.setCurrentCell(self.currentRow() + 1, 0)
        
    def save_progress(self):
        with open("companies.csv", "w", newline='') as f:
            writer = csv.writer(f)
            for row in range(self.rowCount() - 1):
                if (self.item(row, 0) is not None):
                    writer.writerow([self.item(row, 0).text()])
            f.close()
    
    
class CSVView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.csv_widget = CSVWidget()
        vertical_layout = QtWidgets.QVBoxLayout()
        
        horizontal_layout_widget = QWidget()
        horizontal_layout = QtWidgets.QHBoxLayout()
        import_button = QPushButton("Import")
        export_button = QPushButton("Export")
        reset_button = QPushButton("Reset")
        import_button.clicked.connect(self.import_csv)
        export_button.clicked.connect(self.export_csv)
        reset_button.clicked.connect(self.reset_csv)
        
        horizontal_layout.addWidget(import_button)
        horizontal_layout.addWidget(export_button)
        horizontal_layout.addWidget(reset_button)
        horizontal_layout_widget.setLayout(horizontal_layout)
        
        vertical_layout.addWidget(horizontal_layout_widget)
        vertical_layout.addWidget(self.csv_widget)
        self.setLayout(vertical_layout)
    
    def export_csv(self):
        pass

    def import_csv(self):
        dir_dialog = QFileDialog()
        if dir_dialog.exec():
            file_name = dir_dialog.selectedFiles()
        self.csv_widget.clearContents()
        
    def reset_csv(self):
        assurance = QMessageBox(self)
        assurance.setWindowTitle("Reset")
        assurance.setText("Reset the table?")
        assurance.setStandardButtons(QMessageBox.Reset | QMessageBox.Cancel)
        ret = assurance.exec()
        
        match ret:
            case QMessageBox.Reset:
                self.csv_widget.clearContents()
            

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
    
        