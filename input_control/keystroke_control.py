import keyboard
from keyboard import KeyboardEvent

from protocol.protocol import *


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

    @staticmethod
    def transmit(sock):
        last_one = None
        while True:
            keystroke = KeyStrokes.record()
            if keystroke != last_one:
                print(keystroke, last_one)
                packet = Packet(PacketType.KEYBOARD, keystroke.encode())
                SendPacket.send_packet(sock, packet)
                last_one = keystroke

