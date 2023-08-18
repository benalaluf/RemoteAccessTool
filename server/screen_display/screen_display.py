from tkinter import Image

from PIL import Image, ImageTk
import tkinter as tk


class ScreenDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display App")

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.current_image = None
        self.update_image("../connection/image.png")

    def update_image(self, image):
        self.current_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.current_image)
