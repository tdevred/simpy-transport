from collections import namedtuple
from typing import Tuple, Type, overload, Dict
from node import Node

Edge = namedtuple('Edge', ['origin', 'destination', 'length'])

class Graph:

    def __init__(self, isDirected=False):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[Tuple[str, str], Edge] = {}
        self.isDirected = isDirected

    def addEdge(self, n1, n2, length:float):

        if not isinstance(n1, (Node, str)) or not isinstance(n2, (Node, str)):
            raise TypeError('Arguments must be Nodes or str')

        if isinstance(n1, str):
            try:
                n1 = self.getNode(n1)
            except KeyError as e:
                raise e
        if isinstance(n2, str):
            try:
                n2 = self.getNode(n2)
            except KeyError as e:
                raise e

        self.edges[(n1.id, n2.id)] = Edge(
            n1.id,
            n2.id,
            length
        )
        if not self.isDirected:
            self.edges[(n2.id, n1.id)] = Edge(
                n2.id,
                n1.id,
                length
            )

    def getNode(self, name:str):
        if name not in self.nodes:
            return KeyError(f'{name} is not a valid not in graph')
        return self.nodes[name]

    def getEdges(self, n1:str, n2:str):
        return [edge for key, edge in self.edges.items() if key == (n1, n2)]

    def getEdgesFrom(self, n:str):
        if self.isDirected:
            return [edge for key, edge in self.edges.items() if key[0] == n]
        else:
            return self.getEdgesConcerning(n)

    def getEdgesTo(self, n:str):
        if self.isDirected:
            return [edge for key, edge in self.edges.items() if key[1] == n]
        else:
            return self.getEdgesConcerning(n)

    def getEdgesConcerning(self, n:str):
        return [edge for key, edge in self.edges.items() if n in key]

    def addNode(self, node:Node):
        self.nodes[node.id] = node

    def __add__(self, other):
        if not isinstance(other, Graph):
            raise TypeError('Other must be a Graph')
        
        if self.isDirected == other.isDirected:
            result = Graph()
            result.nodes = {**self.nodes, **other.nodes}
            result.edges = {**self.edges, **other.edges}
            return result
        else:
            return self.getDirectedForm() + other.getDirectedForm()

    def absorb(self, other):
        if not isinstance(other, Graph):
            raise TypeError('Other must be a Graph')
        
        if self.isDirected == other.isDirected:
            self.nodes.update(other.nodes)
            self.edges.update(other.edges)
        else:
            if not self.isDirected:
                raise ValueError('Cannot merge undirected with directed graph')
            self.nodes.update(other.nodes)
            self.edges.update(other.edges)

    def copy(self):
        g = Graph(self.isDirected)
        g.nodes = self.nodes.copy()
        g.edges = self.edges.copy()
        return g

    def getDirectedForm(self):
        if self.isDirected:
            return self.copy()
        else:
            g = Graph(True)
            g.nodes = self.nodes.copy()
            for key, value in self.edges.items():
                g.edges[key] = value
                g.edges[key[::-1]] = Edge(
                    value.destination,
                    value.origin,
                    value.length
                )
            return g

# TESTS
if __name__ == '__main__':
    g1 = Graph()
    g1.addNode(Node('1'))
    g1.addNode(Node('2'))
    g1.addEdge('1', '2', 40)
    print(g1.nodes, g1.edges)

    g2 = Graph()
    g2.addNode(Node('3'))
    g2.addNode(Node('4'))
    g2.addEdge('3', '4', 10)
    print(g2.nodes, g2.edges)

    g3 = g1 + g2
    print(g3.nodes, g3.edges)

    g1.absorb(g2)
    print(g1.nodes, g1.edges)
