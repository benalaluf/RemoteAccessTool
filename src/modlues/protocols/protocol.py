import socket
import struct
from abc import ABC, abstractmethod
from ctypes import Union
from enum import Enum


class PacketConstants:
    TYPE_HEADER_FORMAT = '>B'  # big-big-endian unsigned char
    PAYLOAD_LENGTH_HEADER_FORMAT = '>I'  # big-endian unsigned int
    HEADER_LENGTH = 6  # bytes


class PacketType(Enum):
    GENERAL = 1
    REMOTE_SHELL = 2
    REMOTE_DESKTOP = 3


class Packet(ABC):
    def __init__(self, packet_type: Union(PacketType, int), packet_sub_type, payload: bytes):
        self.packet_type = packet_type
        self.packet_sub_type = packet_sub_type
        self.payload = payload
        self.packet_bytes = bytes()

    @classmethod
    def from_bytes(cls, byte: bytes):
        packet_type = struct.unpack(PacketConstants.TYPE_HEADER_FORMAT, byte[0])[0]
        packet_sub_type = struct.unpack(PacketConstants.TYPE_HEADER_FORMAT, byte[1])[0]
        data_len = struct.unpack(PacketConstants.TYPE_HEADER_FORMAT, byte[2:])[0]
        payload = byte[data_len:]

        return cls(packet_type, packet_sub_type, payload)

    def __bytes__(self):
        return self._build_packet()

    def _build_packet(self):
        self.packet_bytes = self._pack(PacketConstants.TYPE_HEADER_FORMAT, self.packet_type.value) + \
                            self._pack(PacketConstants.TYPE_HEADER_FORMAT, self.packet_sub_type.value) + \
                            self._pack(PacketConstants.PAYLOAD_LENGTH_HEADER_FORMAT, (len(self.payload))) + \
                            self.payload

    # !NIMI
    def _pack(self, pack_format, data):
        return struct.pack(pack_format, data)


class SendPacket:

    @staticmethod
    def send_packet(sock: socket.socket, packet: Packet):
        sock.sendall(bytes(packet))


class HandelPacket:

    @staticmethod
    def recv_packet(sock):
        return Packet.from_bytes(HandelPacket.__recv_raw_packet(sock))

    @staticmethod
    def __recv_raw_packet(sock):
        raw_header = HandelPacket.__recv_all(sock, PacketConstants.HEADER_LENGTH)

        if not raw_header:
            return None

        data_len = struct.unpack(PacketConstants.TYPE_HEADER_FORMAT, raw_header[2:])[0]
        data = HandelPacket.__recv_all(sock, data_len)

        return raw_header + data

    @staticmethod
    def __recv_all(sock, data_len):
        data = bytearray()
        while len(data) < data_len:
            packet = sock.recv(data_len - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
