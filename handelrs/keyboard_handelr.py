from input_control.keystroke_control import KeyStrokes


class HandelKeyboard:

    @staticmethod
    def handel(payload: bytes):
        payload = payload.decode()
        payload = payload.split()
        print(payload)
        KeyStrokes.play(payload)