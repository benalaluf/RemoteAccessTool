import socket
import struct
from abc import ABC, abstractmethod
from enum import Enum


class PacketType(Enum):
    FRAME = 1
    KEYBOARD = 2
    MOUSE = 3
    EXIT = 4294967295


class Packet:
    def __init__(self, packet_type: PacketType, payload: bytes):
        self.TYPE_HEADER_LENGTH = 4
        self.PAYLOAD_LENGTH_HEADER_LENGTH = 4
        self.packet_type = packet_type
        self.payload = payload

    def __bytes__(self):
        return self._create_packet()

    def _create_packet(self):
        packet = self.__pack(self.packet_type.value) + self.__pack((len(self.payload))) + self.payload
        return packet

    def __pack(self, data):
        return struct.pack('>I', data)


class SendPacket:

    @staticmethod
    def send_packet(sock: socket.socket, packet: Packet):
        sock.sendall(bytes(packet))


class HandelPacket:

    @staticmethod
    def recv_packet(sock):
        return HandelPacket.__recv_packet_type(sock), HandelPacket.__recv_payload(sock)

    @staticmethod
    def __recv_packet_type(sock):
        raw_type = HandelPacket.__recvall(sock, 4)
        if not raw_type:
            return None
        type = struct.unpack('>I', raw_type)[0]
        return type

    @staticmethod
    def __recv_payload(sock):
        raw_data_lenght = HandelPacket.__recvall(sock, 4)
        if not raw_data_lenght:
            return None
        data_lenght = struct.unpack('>I', raw_data_lenght)[0]
        return HandelPacket.__recvall(sock, data_lenght)

    @staticmethod
    def __recvall(sock, data_len):
        data = bytearray()
        while len(data) < data_len:
            packet = sock.recv(data_len - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

