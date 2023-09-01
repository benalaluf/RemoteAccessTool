from src.connections.victim import Victim

if __name__ == '__main__':
    print("run vicim")
    victim = Victim("localhost", 21211).main()
    print("runned victim")