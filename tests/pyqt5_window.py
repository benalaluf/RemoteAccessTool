import threading
import tkinter as tk
from multiprocessing import Process

from PIL import Image, ImageTk
import time

class ImageDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display App")

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        self.current_image = None
        self.update_image("../server/connection/image.png")

    def update_image(self, image_path):
        image = Image.open(image_path)
        self.current_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.current_image)


class updater:

    def __init__(self, app):
        self.app = app
        self.last_one = 1

    def update(self,):
        if self.last_one == 1:
            app.update_image('image2.png')
            self.last_one = 2
        else:
            app.update_image('image.png')
            self.last_one = 1
        self.app.root.after(1000, self.update,)




if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDisplayApp(root)
    updater = updater(app)

    updater.update()


    root.mainloop()
