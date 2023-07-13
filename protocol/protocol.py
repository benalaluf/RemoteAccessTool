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


class HandelPacket:

    def recv_packet(self, sock):
        return self.__recv_packet_type(sock), self.__recv_payload()

    def __recv_packet_type(self, sock):
        raw_type = self.__recvall(sock, 4)
        if not raw_type:
            return None
        type = struct.unpack('>I', raw_type)[0]
        return type

    def __recv_payload(self, sock):
        raw_data_lenght = self.__recvall(sock, 4)
        if not raw_data_lenght:
            return None
        data_lenght = struct.unpack('>I', raw_data_lenght)[0]
        return self.__recvall(sock, data_lenght)

    def __recvall(self, sock, data_len):
        data = bytearray()
        while len(data) < data_len:
            packet = sock.recv(data_len - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
