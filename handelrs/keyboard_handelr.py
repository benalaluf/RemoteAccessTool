from input_control.keystroke_control import KeyStrokes


class HandelKeyboard:

    #example
    @staticmethod
    def handel(payload):
        payload = payload.decode()
        KeyStrokes.play(payload)