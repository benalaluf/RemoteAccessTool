import time
import tkinter
from tkinter import Tk, Canvas, ttk

from PIL import ImageGrab, ImageTk, Image


class ScreenCapture:

    def __init__(self, screen_size, screen_mode):
        self.screen_size = screen_size
        self.screen_mode = screen_mode
        self.current_screen = None

    def image_from_bytes(self, bytes):
        return Image.frombytes(self.screen_mode, self.screen_size, bytes)

    def image_to_bytes(self, image):
        return image.tobytes()

    def take_screenshot(self):
        return ImageGrab.grab()

    def frame_bytes(self):
        return self.image_to_bytes(self.take_screenshot())
