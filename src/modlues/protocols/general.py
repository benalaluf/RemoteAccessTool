from enum import Enum

from src.modlues.protocols.protocol import Packet, PacketType, PacketConstants


class GeneralPacketType(Enum):
    ACK = 0
    CONNECT_RSH = 1
    CONNECT_RD = 2
    EXIT = 3


class GeneralPacket(Packet):
    def __init__(self, packet_sub_type: GeneralPacketType, payload: bytes = PacketConstants.NO_DATA):
        super().__init__(PacketType.GENERAL, packet_sub_type.value, payload)
