from src.connections.victim import Victim

if __name__ == '__main__':
    print("run vicim")
    victim = Victim("0.0.0.0", 8105).main()
    print("runned victim")