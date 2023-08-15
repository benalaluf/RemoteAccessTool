import threading

from protocol.protocol import Packet, SendPacket, PacketType
from screen_mirroring.screen_capture import ScreenCapture
from screen_mirroring.screen_window import ScreenWindow


class ScreenStream:

    @staticmethod
    def transmit_frame(sock, addr):
        frame_bytes = ScreenCapture.frame_bytes()
        packet = Packet(PacketType.FRAME, frame_bytes)
        SendPacket.send_packet(sock, packet)

    @staticmethod
    def receive_frame(screen_window: ScreenWindow, payload: bytes):
        frame = ScreenCapture.bytes_to_frame(bytes(payload))
        screen_window.set_frame(frame)
