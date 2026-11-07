from gui.overlay import Overlay
from PIL import ImageGrab
from threading import Event

import cv2, pytesseract, threading, time


class ProcessImg():
    def __init__(self):
        self.img_path = "screengrabs/view.png"
        self.exit_thread = Event()
        self.overlay = Overlay()
        self.overlay.change_ui.connect(self.test)
        
    def test(self, data):
        self.overlay.highlight_area(data)
    
    def grab_screen(self):  
        while not self.exit_thread.is_set():
            self.overlay.clear_flag = 1
            self.overlay.update() # Clears the overlay for clean screen capture
            time.sleep(0.5) # Grace period for screen grab
            screenshot = ImageGrab.grab()
            screenshot.save(self.img_path, quality=100)
            img = cv2.imread(self.img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            data = pytesseract.image_to_data(img_rgb, output_type=pytesseract.Output.DICT)
            self.overlay.change_ui.emit(data)
            self.exit_thread.wait(5)
        
    def launch_thread(self, activate):
        thread = threading.Thread(target=self.grab_screen)
        if not activate:
            self.exit_thread.set()
        else:
            self.exit_thread.clear()
            thread.start()
            
    def kill_thread(self):
        self.exit_thread.set()