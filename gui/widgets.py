from processing.ocr import ProcessImg
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog, QMessageBox, QPushButton, QWidget

import csv


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
        dir_dialog = QFileDialog()
        dir_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dir_dialog.setNameFilter("CSV File (*.csv)")
        if dir_dialog.exec():
            file_name = dir_dialog.selectedFiles()
            with open(file_name[0], "wt", newline='') as f:
                writer = csv.writer(f)
                for row in range(self.csv_widget.rowCount() - 1):
                    if (self.csv_widget.item(row, 0) is not None):
                        writer.writerow([self.csv_widget.item(row, 0).text()])
                f.close()

    def import_csv(self):
        dir_dialog = QFileDialog()
        dir_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dir_dialog.setNameFilter("CSV Files (*.csv)")
        if dir_dialog.exec():
            file_name = dir_dialog.selectedFiles()
            self.csv_widget.clearContents()
            with open(file_name[0], "rt") as f:
                row = 0
                reader = csv.reader(f)
                for line in reader:
                    item = QtWidgets.QTableWidgetItem(line[0])
                    self.csv_widget.setItem(row, 0, item)
                    row += 1
                    self.csv_widget.expand_row()
                f.close()
            
    def reset_csv(self):
        assurance = QMessageBox(self)
        assurance.setWindowTitle("Reset")
        assurance.setText("Reset the table?")
        assurance.setStandardButtons(QMessageBox.Reset | QMessageBox.Cancel)
        ret = assurance.exec()
        
        match ret:
            case QMessageBox.Reset:
                self.csv_widget.clearContents()
                              
                
class OverlayWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        self.process_img = ProcessImg()
        
        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.activate_button = QtWidgets.QPushButton("Activate Overlay")
        self.activate_button.setCheckable(True)
        self.activate_button.toggled.connect(self.activate_overlay)
        
        self.layout.addWidget(self.activate_button)
        
    def activate_overlay(self):
        activate = self.activate_button.isChecked()
        self.process_img.launch_thread(activate)
    
    def kill_thread_on_close(self):
        self.process_img.kill_thread()
            
        
class CentralWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        
        self.overlay_widget = OverlayWidget()
        self.csv_view = CSVView()
        
        self.addTab(self.overlay_widget, "Overlay")
        self.addTab(self.csv_view, "Companies")
        
    def kill_thread_on_close(self):
        self.overlay_widget.kill_thread_on_close()
    
        
    
        