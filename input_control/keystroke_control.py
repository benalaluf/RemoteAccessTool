import keyboard
from keyboard import KeyboardEvent


class KeyStrokes:

    @staticmethod
    def record():
        event = str(keyboard.read_event())
        event = event.removeprefix(r'KeyboardEvent(')
        event = event.removesuffix(')')
        return event

    @staticmethod
    def play(event: list):
        key = event[0]
        state = event[1]

        if state == 'up':
            keyboard.press(key)
        if state == 'down':
            keyboard.release(key)
