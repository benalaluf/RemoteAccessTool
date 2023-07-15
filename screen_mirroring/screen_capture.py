import time
import tkinter
from tkinter import Tk, Canvas, ttk

from PIL import ImageGrab, ImageTk, Image


class ScreenCapture:

    @staticmethod
    def frame_bytes():
        return ScreenCapture.__image_to_bytes(ScreenCapture.__take_screenshot())

    @staticmethod
    def bytes_to_frame(bytes, screen_mode, screen_size):
        return ScreenCapture.__image_to_tkImage(ScreenCapture.__image_from_bytes(bytes, screen_mode, screen_size))

    @staticmethod
    def __image_to_bytes(image):
        return image.tobytes()

    @staticmethod
    def __image_from_bytes(bytes, screen_mode, screen_size):
        return Image.frombytes(screen_mode, screen_size, bytes)

    @staticmethod
    def __take_screenshot():
        return ImageGrab.grab()

    @staticmethod
    def __image_to_tkImage(image):
        return ImageTk.PhotoImage(image)
