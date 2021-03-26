from path import Dijkstra, computePath
from passenger import Passenger
from typing import List
from graph import Graph
from line import Line
from random import sample

class Kernel:
    
    def __init__(self, env) -> None:
        self.env = env

        self.lines: List[Line] = []
        self.graph = Graph(True)
        self.passengers: List[Passenger] = []

    def addLine(self, line:Line):
        self.lines.append(line)
        line.bindEnv(self.env)
        self.graph.absorb(line.graph)

    def addInterconnection(self, n1:str, n2:str, length:float):
        self.graph.addEdge(n1, n2, length)

    def run(self):
        for line in self.lines:
            line.run()

    def buildPassengers(self, count:int):
        result = {}
        
        for line in self.lines:
            for node in line.nodes:
                result[node.id] = Dijkstra(node.id, self.graph)

        self.passengers = [
            *buildPassengers(count, result, self.lines)
        ]

        self.placePassengers()
        

    def placePassengers(self):
        for passenger in self.passengers:
            node = self.graph.nodes[passenger.path.nodes[0]]
            node.addWaitingStart(passenger)

    def buildTransports(self):
        for line in self.lines:
            line.buildTransports()

def buildPassengers(count, result, lines):
    for i in range(count):
        p = Passenger(i, getRandomPath(result, [node.id for line in lines for node in line.nodes]))
        yield p

def getRandomPath(res, nodes:List[str]):
    while True:
        origin, dest = sample(nodes, 2)
        path = computePath(dest, res[origin][1])
        if path:
            return path