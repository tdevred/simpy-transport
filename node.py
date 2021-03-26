from random import choice
from passenger import Passenger
from typing import List
from queue import Queue
from utils import Way

class Node:
    def __init__(self, id_node:str) -> None:
        self.id = id_node
        self.waiting: List[Passenger] = {
            Way.UP: Queue(),
            Way.DOWN: Queue()
        }
        self.shop = None
        self.env = None
    def __repr__(self) -> str:
        return f'Node {self.id}'

    def addWaiting(self, passenger: Passenger):
        if self.shop and choice([True]*1 + [False]*4):
            print('should wait')
            yield self.env.process(self.shop.action(passenger))

        print(f'{passenger!r} is waiting at {passenger.getNode()}')
        self.waiting[passenger.path.getWay()].put(passenger)

    def addWaitingStart(self, passenger: Passenger):
        self.waiting[passenger.path.getWay()].put(passenger)

    def getWaiting(self, way:Way):
        return self.waiting[way]

    def bindEnv(self, env):
        self.env = env