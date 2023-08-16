import keyboard


class KeyboardReceiver:

    #TODO add multipul key press like ctrl+c
    @staticmethod
    def play(event: list):
        key = event[0]
        state = event[1]

        if state == 'up':
            keyboard.press(key)
        if state == 'down':
            keyboard.release(key)