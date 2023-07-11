import keyboard


class KeyStrokes:

    @staticmethod
    def record():
        return keyboard.read_event()

    @staticmethod
    def play(event):
        keyboard.play((event,))
