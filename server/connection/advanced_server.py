import socket

import threading
import tkinter as tk

from modoules.protocol.protocol import Packet, PacketType, SendPacket, HandelPacket
from server.input_handling.keyboard_control import KeyboardControl
from server.screen_display.screen_display import ScreenDisplay
from server.screen_display.screen_receiver import ScreenReceiver


class Server:

    def __init__(self, ip, port):
        self.root = tk.Tk()
        self.screen_display = ScreenDisplay(self.root)
        self.IP = ip
        self.PORT = port
        self.ADDR = (ip, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.connected_clients_number = 0
        self.connected_clients = dict()

        self.current_client = None

        thread = threading.Thread(target=self.start_listing)
        thread.start()

        self.main()
        self.root.mainloop()

    def start_listing(self):
        self.server.listen()
        print(f'LISTENING... ({self.IP}:{self.PORT})')
        admin_control = threading.Thread(target=self.__admin_input)
        admin_control.start()
        try:
            while True:
                conn, addr = self.server.accept()
                print(f'connection from: {addr}')
                self.__on_new_client(conn, addr)
        except Exception as e:
            print(e)
            self.server.close()

    def main(self):
        if self.current_client:
            self.transmit_keyboard_control(self.current_client[0])
            self.transmit_mouse_control(self.current_client[0])
            type, bytes = HandelPacket.recv_packet(self.current_client[0])
            if type == PacketType.FRAME.value:
                frame = ScreenReceiver.bytes_to_frame(bytes)
                self.screen_display.update_image(frame)

        self.root.after(10, self.main)

    def transmit_keyboard_control(self, conn):
        event = KeyboardControl.record()
        packet = Packet(PacketType.KEYBOARD, event.encode())
        SendPacket.send_packet(conn, packet)

    def transmit_mouse_control(self, conn):
        pass

    def handel(self, client):
        self.current_client = client
        packet = Packet(PacketType.START, 'start'.encode())
        SendPacket.send_packet(client[0], packet)

    def __on_new_client(self, conn, addr):
        self.connected_clients_number += 1
        self.connected_clients.update({str(self.connected_clients_number): (conn, addr)})

    def __choose_client(self, args: list):
        if args[0] in self.connected_clients.keys():
            client = self.connected_clients[args[0]]
            self.handel(client)

    def __print_connected_clients(self, args: list = None):
        for cid, client in self.connected_clients.items():
            print(f'{cid}. - {client[1]}')

    def __help(self, args: list = None):
        print('get some help')

    def __admin_input(self):
        while True:
            command = input('$ ')

            command_components = command.split(' ')
            command = command_components[0]
            command_args = command_components[1:]

            if command in Server.commands.keys():
                Server.commands[command](self, command_args)
            else:
                print('try help')

    commands = {
        "ls": __print_connected_clients,
        "choose": __choose_client,
        "help": __help,
    }


if __name__ == '__main__':
    print('SERVER IS STARTING :)')

    server = Server('localhost', 2221)
    server.start_listing()
