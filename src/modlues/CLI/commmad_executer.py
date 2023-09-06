from src.modlues.CLI.print_enchanter import segement_print


class CommandExecuter:
    def __init__(self, commands: dict):
        self.commands = commands

    def exec(self, command: str):

        command = command.split(' ')
        command_parms = command[1:]

        func = self.commands.get(command[0])

        if func:
            func(command_parms)

        if command == "help":
            self.__print_available_commands()
        else:
            print(f'{command} is unknown, try "help"')

    @segement_print
    def __print_available_commands(self):
        print("The available commands are: ")
        for command in self.commands:
            print(f'- "{command}"')
