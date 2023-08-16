import keyboard



class KeyboardControl:

    @staticmethod
    def record():
        event = str(keyboard.read_event())
        event = event.removeprefix(r'KeyboardEvent(')
        event = event.removesuffix(')')
        return event
