import tkinter
from tkinter import Tk, Canvas

from PIL import ImageGrab, ImageTk


class ScreenShare:

    def __init__(self):
        self.current_screen = None

    def take_screenshot(self):
        self.current_screen = ImageGrab.grab()

    def display(self):
        root = Tk()
        root.geometry('1980x1080')
        canvas = Canvas(root, width=1980, height=1080)
        canvas.pack()

        self.take_screenshot()
        image = ImageTk.PhotoImage(self.current_screen)
        canvas.create_image(0, 0, image=image, anchor=tkinter.NW)
        root.mainloop()


if __name__ == '__main__':
    ScreenShare().display()
