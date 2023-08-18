import time
import tkinter
from io import BytesIO
from tkinter import Tk, Canvas, ttk

from PIL import ImageGrab, ImageTk, Image


class ScreenReceiver:

    @staticmethod
    def bytes_to_frame(bytes):
        return ScreenReceiver.__image_to_tkImage(ScreenReceiver.__image_from_bytes(bytes))

    @staticmethod
    def __image_from_bytes(bytes):
        return Image.open(BytesIO(bytes))

    @staticmethod
    def __image_to_tkImage(image):
        return ImageTk.PhotoImage(image)
