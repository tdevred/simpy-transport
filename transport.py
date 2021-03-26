from passenger import Passenger
from typing import List
from utils import State, Way
from node import Node

class Transport:

    NAME = "Transport"

    def __init__(self, id_transport:str, line, env, delay, capacity, stop_time) -> None:
        self.env = env
        
        self.id = id_transport
        self.line = line

        self.node_id = 0
        self.way = Way.UP

        self.passengers: List[Passenger] = []
        self.capacity = capacity
        self.stop_time = stop_time

        self.delay = delay

    def getLineId(self):
        return self.line.id

    def __repr__(self) -> str:
        return f'{self.__class__.NAME}: {self.id}'

    def getDistanceToNextNode(self):
        return self.line.getDistance(self.node_id, self.node_id + (1 if self.way == Way.UP else -1))

    def nextNode(self):
        self.node_id += 1 if self.way == Way.UP else -1

    def isAtEnd(self):
        if self.way == Way.UP:
            return self.node_id == len(self.line.nodes)-1
        else:
            return self.node_id == 0

    def start(self):
        yield self.env.timeout(self.delay)
        self.env.process(self.run())

    def run(self):
        yield self.env.timeout(self.stop_time)
        self.takePassengers()

        yield self.env.timeout(self.getDistanceToNextNode())
        self.nextNode()
        print(f'{self!r} at {self.line.nodes[self.node_id]!r} of {self.line!r}')

        if self.isAtEnd():
            print(f'{self!r} is flipping.')
            yield self.env.process(self.flip())

        self.updatePassengers()
        self.deliverPassengers()
            
        yield self.env.process(self.run())

    def flip(self):
        self.way = Way.UP if self.way == Way.DOWN else Way.DOWN
        yield self.env.timeout(self.line.flip_duration)

    def canTakePassenger(self):
        return len(self.passengers) < self.capacity

    def getCurrentNode(self):
        return self.line.nodes[self.node_id]

    def takePassengers(self):
        node = self.getCurrentNode()

        waiting = node.getWaiting(self.way)

        while(self.canTakePassenger() and not waiting.empty()):
            passenger = waiting.get()
            print(f'{self!r} has taken {passenger!r} at {node!r}')
            self.passengers.append(passenger)

    def deliverPassengers(self):
        needingToLeave = [passenger for passenger in self.passengers if passenger.needsToLeaveNext()]
        for passenger in needingToLeave:
            self.passengers.remove(passenger)

            if not passenger.path.isOver():
                node = self.line.nodes[self.node_id]
                self.env.process(node.addWaiting(passenger))
            else:
                print(f'{passenger!r} has ended their journey !')

    def updatePassengers(self):
        for passenger in self.passengers:
            passenger.nextNode()