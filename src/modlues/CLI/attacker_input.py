class AttackerInput:
    def __init__(self, commands: dict):
        self.commands = commands


    def get(self):
        raw_command = input("Attacker $: ")
        command = raw_command.split(' ')
        args = command[1:]

        func = self.commands.get(command[0])
        if func:
            func(args)
        else:
            print(f'{command[0]} is unknown, try help')


