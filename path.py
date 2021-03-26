from typing import Dict, List
from node import Node
from graph import Graph
from math import inf
from utils import Way

class Path:
    def __init__(self):
        self.nodes: List[Node] = []
        self.index = 0

    def nextNode(self):
        if self.isOver():
            raise "CCC"
        self.index += 1

    def getNextSubPath(self):
        return (self.nodes[self.index], self.nodes[self.index+1])

    def isOver(self):
        return self.index == len(self.nodes)-1

    def getWay(self):
        if self.isOver():
            raise "AAA"
        n1 = self.nodes[self.index]
        n2 = self.nodes[self.index+1]
        return Way.UP if int(n1.split('_')[1]) < int(n2.split('_')[1]) else Way.DOWN

    def isOnSameLine(self):
        if self.isOver():
            raise "BBB"
        n1 = self.nodes[self.index]
        n2 = self.nodes[self.index+1]
        return n1.split('_')[0] == n2.split('_')[0]


    def needsToLeaveNext(self):
        return self.isOver() or not self.isOnSameLine()

    def currentNode(self):
        return self.nodes[self.index]

def Dijkstra(origin:str, graph:Graph):

    P = set()

    d: Dict[str, float] = {n: inf for n in graph.nodes}
    d[origin] = 0
    prec: Dict[str, str] = {n: None for n in graph.nodes}
    prec[origin] = origin

    while any((n not in P for n in graph.nodes)):
        temp = {k: v for k, v in d.items() if k not in P}
        a = min(temp, key=lambda n: temp[n])
        P.add(a)
        for edge in graph.getEdgesFrom(a):
            b = edge.destination

            if b not in P:
                distance = edge.length
                if d[b] > d[a] + distance:
                    d[b] = d[a] + distance
                    prec[b] = a

    return d, prec

def computePath(dest:Dict[str, int], prec: Dict[str, str]) -> Path:

    path = Path()

    current = dest
    if prec[current] is None:
        return None

    while current is not None and prec[current] != current:

        path.nodes.append(current)
        current = prec[current]
        if prec[current] is None:
            return None

    path.nodes.append(current)

    return path
