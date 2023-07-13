import keyboard
from keyboard import KeyboardEvent


class KeyStrokes:

    @staticmethod
    def record():
        return keyboard.read_event()

    @staticmethod
    def play(event):
        keyboard.play((event,))


if __name__ == '__main__':
    keyboard.press_and_release('d')