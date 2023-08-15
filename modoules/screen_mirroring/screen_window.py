import tkinter as tk

from utils.singletone import Singleton


class ScreenWindow(metaclass=Singleton):
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('1920x1080')

        self.frame = tk.Label(self.window)
        self.frame.pack()

    def run(self):
        self.window.mainloop()

    def set_frame(self, frame):
        self.frame.image = frame
        self.frame.config(image=frame)
        self.window.update()

