import threading
import tkinter as tk

#TODO add single tone
class ScreenWindow(threading.Thread):
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('1920x1080')

        self.frame = tk.Label(self.window)
        self.frame.pack()
        threading.Thread.__init__(self)
    def run(self):
        self.window.mainloop()

    def set_frame(self, frame):
        self.frame.image = frame
        self.frame.config(image=frame)
        self.window.update()

