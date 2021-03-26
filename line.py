from typing import List
from node import Node
from graph import Graph
from transport import Transport

DELAY_BETWEEN_TR = 50
TRANSPORT_CAPACITY = 10
STOP_TIME = 2
FLIP_DURATION = 2

class Line:
    def __init__(self, name:str, transport_count:int, transport_capacity=TRANSPORT_CAPACITY, stop_time=STOP_TIME, flip_duration=FLIP_DURATION) -> None:
        self.env = None
        self.name = name
        self.nodes: List[Node] = []
        self.graph = Graph(False)
        self.transports: List[Transport] = []
        self.flip_duration = flip_duration
        self.transport_info = {
            'capacity': transport_capacity,
            'stop_time': stop_time,
            'count': transport_count
        }

    def addNode(self, name:str, duration:float=None):
        isFirstNode = not self.nodes

        if not isFirstNode and duration is None:
            raise ValueError('Duration cannot be None (Not first node)')
        
        node = Node(f'{self.name}_{name}')

        self.nodes.append(node)
        self.graph.addNode(node)
            
        if not isFirstNode:
            self.graph.addEdge(self.nodes[-2], node, duration)


    def buildTransports(self):
        self.transports = [
            Transport(str(i), self, self.env, DELAY_BETWEEN_TR*i, self.transport_info['capacity'], self.transport_info['stop_time'])
            for i in range(1, self.transport_info['count']+1)
        ]
        del self.transport_info

    def getDistance(self, s1:int, s2:int):
        edges = self.graph.getEdges(self.nodes[s1].id, self.nodes[s2].id)
        return edges[0].length

    def run(self):
        for transport in self.transports:
            transport.start()

        for transport in self.transports:
            self.env.process(transport.run())

    def __repr__(self) -> str:
        return f'Line {self.name}'

    def bindEnv(self, env):
        self.env = env
        for node in self.nodes:
            node.bindEnv(self.env)