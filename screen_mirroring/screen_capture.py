import time
import tkinter
from tkinter import Tk, Canvas, ttk

from PIL import ImageGrab, ImageTk, Image



class ScreenShare():

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
        return ImageGrab.grab()

    def frame_bytes(self):
        return self.image_tobytes(self.take_screenshot())

    def screen_display(self):
        self.window = tkinter.Tk()

        # Set the window title
        self.window.title("Screen Share")

        # Set the window size to the screen resolution
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}")

        # Create a label to display the screen capture
        self.screen_label = tkinter.Label(self.window)
        self.screen_label.pack()

        # Start the screen sharing

        # Run the Tkinter event loop
        self.window.mainloop()

    def update_screen(self,frame):
        # Capture the screen

        # Update the label with the new image
        self.screen_label.configure(image=frame)
        self.screen_label.image = frame

        # Schedule the next update
        self.window.after(1000 // 30, self.update_screen)
        # Update every 1/30th of a second (30 FPS)