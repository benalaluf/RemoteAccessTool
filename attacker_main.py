from src.connections.attacker import Attacker

if __name__ == '__main__':
    attacker = Attacker("localhost", 2111).main()
    print("runned attacker")