import threading
import time
from multiprocessing import Process

from modoules.screen_mirroring.screen_window import ScreenWindow

if __name__ == '__main__':
    tk_window = ScreenWindow()
    tk_window.start()
    tk_window.run()
    while True:
        print(threading.current_thread().name)
        time.sleep(10)
