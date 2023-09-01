from src.connections.victim import Victim

if __name__ == '__main__':
    print("run vicim")
    victim = Victim("localhost", 2211).main()
    print("runned victim")