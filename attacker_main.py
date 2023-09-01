from src.connections.attacker import Attacker

if __name__ == '__main__':
    attacker = Attacker("localhost", 21211).main()
    print("runned attacker")