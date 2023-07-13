import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO

from screen_mirroring.screen_capture import ScreenCapture
from utils.singletone import Singleton


class ScreenWindow(metaclass=Singleton):
    def __init__(self):
        self.current_frame = None
        self.window = tk.Tk()
        self.window.geometry('1920x1080')

        self.label = tk.Label(self.window)
        self.label.pack()

        self.window.mainloop()

    def set_frame(self):
        self.label.image = ScreenCapture.frame_bytes(ScreenCapture.frame_bytes())

if __name__ == '__main__':
    
    ScreenWindow()

