import cv2, pytesseract, time, threading

from PIL import ImageGrab
from threading import Event


class ProcessImg():
    exit_thread = Event()
    
    def __init__(self):
        self.img_path = "screengrabs/view.png"
    
    def grab_screen(self):
        while not self.exit_thread.is_set():
            screenshot = ImageGrab.grab();
            screenshot.save(self.img_path)

            img = cv2.imread(self.img_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            data = pytesseract.image_to_string(img_rgb)#pytesseract.image_to_data(img_rgb)
            print(data)
            time.sleep(5)
        
    def launch_thread(self, activate):
        thread = threading.Thread(target=self.grab_screen)
        if not activate:
            self.exit_thread.set()
        else:
            self.exit_thread.clear()
            thread.start()