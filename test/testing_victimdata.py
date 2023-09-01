import socket

from src.modlues.protocols.victim_dataclass import VictimData

one = VictimData(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ("one",3434))
two = VictimData(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ("two", 234))
three = VictimData(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ("three", 3434))
four = VictimData(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ("four",34))

print(one)
print(two)
print(three)
print(four)