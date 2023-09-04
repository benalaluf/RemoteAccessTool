class CommandExecuter:
    def __init__(self, commands: dict):
        self.commands = commands

    def exec(self, command: str):

        func = self.commands.get(command)
        if func:
            func()
        else:
            print(f'{command[0]} is unknown, try help')
