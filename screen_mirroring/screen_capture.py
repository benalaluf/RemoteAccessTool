import time
import tkinter
from io import BytesIO
from tkinter import Tk, Canvas, ttk

from PIL import ImageGrab, ImageTk, Image


class ScreenCapture:

    @staticmethod
    def frame_bytes():
        return ScreenCapture.__image_to_bytes(ScreenCapture.__take_screenshot())

    @staticmethod
    def bytes_to_frame(bytes):
        return ScreenCapture.__image_to_tkImage(ScreenCapture.__image_from_bytes(bytes))

    @staticmethod
    def __image_to_bytes(image):
        imagebytes = BytesIO()
        image.save(imagebytes, format='PNG')
        imagebytes = imagebytes.getvalue()
        return imagebytes

    @staticmethod
    def __image_from_bytes(bytes):
        return Image.open(BytesIO(bytes))

    @staticmethod
    def __take_screenshot():
        return ImageGrab.grab()

    @staticmethod
    def __image_to_tkImage(image):
        return ImageTk.PhotoImage(image)
