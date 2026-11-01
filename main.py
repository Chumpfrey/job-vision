import cv2, pytesseract, threading, sys, time

from PIL import ImageGrab
from matplotlib import pyplot as plt
from gui.application import MyApplication

def grab_screen():
    while True:
        img_path = "0.png"
        screenshot = ImageGrab.grab(all_screens=True);
        screenshot.save(img_path)

        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        data = pytesseract.image_to_data(img_rgb)
        print(data)
        time.sleep(5)
        
if __name__ == "__main__":
    #stop_thread = threading.Event()
    #grab_thread = threading.Thread(target=grab_screen)
    #grab_thread.start()
    #grab_thread.join()
    MyApplication()
    
    
    
