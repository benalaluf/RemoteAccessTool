import time
import tkinter
from tkinter import Tk, Canvas

from PIL import ImageGrab, ImageTk, Image


class ScreenShare:

    def __init__(self, screen_size, screen_mode):
        self.screen_size = screen_size
        self.screen_mode = screen_mode
        self.current_screen = None

    def image_frombytes(self, bytes):
        image = Image.frombytes("RGBA", self.screen_size, bytes)
        image.show()

    def image_tobytes(self, image):
        return image.tobytes()

    def take_screenshot(self):
        self.current_screen = ImageGrab.grab()

    def update(self):
        # inegrate with protocol
        imagebyets = None
        self.current_screen = self.image_frombytes(imagebyets)
        time.sleep(0.01)
        # 60 times a second

    def display(self):
        root = Tk()
        root.geometry('1920x1080')
        canvas = Canvas(root, width=self.screen_size[0], height=self.screen_size[1])
        canvas.pack()
        image = ImageTk.PhotoImage(self.current_screen)
        canvas.create_image(0, 0, image=image, anchor=tkinter.NW)
        root.mainloop()


if __name__ == '__main__':
    # ScreenShare().display()
    screen = ScreenShare((1920, 1080), "RGBA")
    screen.take_screenshot()
    screen.image_frombytes(screen.image_tobytes(screen.current_screen))
