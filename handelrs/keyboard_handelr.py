from input_control.keystroke_control import KeyStrokes


class HandelKeyboard:

    @staticmethod
    def handel(payload: bytes):
        print('handel keyboard')
        payload = payload.decode()
        payload = payload.split()
        KeyStrokes.play(payload)