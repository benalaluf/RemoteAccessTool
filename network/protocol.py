import socket
import struct
from abc import ABC, abstractmethod
from enum import Enum


class PacketType(Enum):
    FRAME = bytes(1),
    KEYBOARD = bytes(2),
    MOUSE = bytes(3),


class Packet:
    def __init__(self, packet_type: PacketType, payload: bytes):
        self.TYPE_HEADER_LENGTH = 4
        self.PAYLOAD_LENGTH_HEADER_LENGTH = 4
        self.packet_type = packet_type
        self.payload = payload

    def __bytes__(self):
        return self._create_packet()

    def _create_packet(self):
        packet = self.__pack(self.packet_type) + self.__pack((len(self.payload))) + self.payload
        return packet

    def __pack(self, data):
        return struct.pack('>I', data)


class SendPacket:

    @staticmethod
    def send_packet(sock: socket.socket, packet: Packet):
        sock.sendall(bytes(packet))


class HandelPacket(ABC):

    @abstractmethod
    def _recv_packet(self, sock):
        pass

    def _recvall(self, sock, data_len):
        data = bytearray()
        while len(data) < data_len:
            packet = sock.recv(data_len - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
