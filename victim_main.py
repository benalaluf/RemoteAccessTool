from src.connections.victim import Victim

if __name__ == '__main__':
    victim = Victim("localhost", 6969).main()
    print("runned victim")