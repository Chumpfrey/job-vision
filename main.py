import cv2, pytesseract, threading

from PIL import ImageGrab
from matplotlib import pyplot as plt

def grab_screen():
    img_path = "0.png"
    screenshot = ImageGrab.grab(all_screens=True);
    screenshot.save(img_path)

    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    data = pytesseract.image_to_data(img_rgb)
    print(data)

def main():
    grab_thread = threading.Thread(target=grab_screen)
    grab_thread.start()
    grab_thread.join()
        
if __name__ == "__main__":
    main()