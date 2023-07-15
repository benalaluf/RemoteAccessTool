import socket
import sys

from protocol.protocol import HandelPacket, PacketType
from screen_mirroring.screen_stream import ScreenStream
from screen_mirroring.screen_window import ScreenWindow

sys.path.append('..')
import threading
from input_control.keystroke_control import KeyStrokes


class Server:

    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port
        self.ADDR = (ip, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.stream_window = ScreenWindow()

    def handel(self, conn):
        while True:
            packet_type, packet_payload = HandelPacket.recv_packet(conn)

            if packet_type == PacketType.FRAME.value:
                ScreenStream.receive_frame(self.stream_window, packet_payload, (1920, 1080), 'RGB')

    def start(self):
        self.server.listen()
        print(f'LISTENING... ({self.IP}:{self.PORT})')
        try:
            while True:
                conn, addr = self.server.accept()
                print('connection from:', addr)
                thread = threading.Thread(target=self.handel, args=(conn,))
                thread.start()
        except Exception as e:
            print(e)
            self.server.close()


if __name__ == '__main__':
    print('SERVER IS STARTING :)')

    server = Server('192.168.1.129', 3333)
    thread = threading.Thread(target=server.start)
    server.stream_window.run()