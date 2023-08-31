from enum import Enum

from src.modlues.protocols.protocol import Packet, PacketType


class RemoteShellPacketType(Enum):
    COMMAND = 1
    SHELL = 2
    OUTPUT = 3


class RemoteShellPacket(Packet):
    def __init__(self, packet_sub_type: RemoteShellPacketType, payload: bytes):
        super().__init__(PacketType.REMOTE_SHELL, packet_sub_type, payload)

