from PySide6 import QtWidgets
from PySide6.QtGui import QCloseEvent
from gui.widgets import CentralWidget

import sys


class MyApplication(QtWidgets.QMainWindow):
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        super().__init__()
        self.central_widget = CentralWidget()
        
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Job Vision")
        
        self.resize(800, 800)
        self.show()
      
        sys.exit(self.app.exec())
    
    def closeEvent(self, event:QCloseEvent):
        self.app.closeAllWindows()
        self.central_widget.kill_thread_on_close()

        return super().closeEvent(event)
    