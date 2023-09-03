from src.connections.victim import Victim

if __name__ == '__main__':
    print("run vicim")
    victim = Victim("localhost", 2111).main()
    print("runned victim")