from loader import Loader
from shop import Sandwicherie, BoutiqueSouvenirs
from kernel import Kernel
from line import Line
import simpy
from random import randint, seed
from sys import argv
import os

def main():
    env = simpy.Environment()

    kernel = Kernel(env)

    l1 = Line('Line1', 10)
    l1.addNode('0')
    for i in range(1, 12):
        l1.addNode(str(i), randint(10, 15))
    
    kernel.addLine(l1)

    l2 = Line('Line2', 10)
    l2.addNode('0')
    for i in range(1, 12):
        l2.addNode(str(i), randint(5, 8))

    kernel.addLine(l2)

    kernel.addInterconnection('Line1_1', 'Line2_2', 20)
    kernel.addInterconnection('Line1_3', 'Line2_10', 20)
    kernel.addInterconnection('Line1_8', 'Line2_1', 20)

    kernel.buildPassengers(1000)

    kernel.graph.nodes['Line1_1'].shop = Sandwicherie(env)
    kernel.graph.nodes['Line2_2'].shop = Sandwicherie(env)

    kernel.graph.nodes['Line1_3'].shop = BoutiqueSouvenirs(env)
    kernel.graph.nodes['Line2_10'].shop = Sandwicherie(env)

    kernel.graph.nodes['Line1_8'].shop = BoutiqueSouvenirs(env)
    kernel.graph.nodes['Line2_1'].shop = BoutiqueSouvenirs(env)

    kernel.buildTransports()
    
    kernel.run()

    env.run(until=1000)

def mainLoading(filename):
    env = simpy.Environment()
    
    kernel = Kernel(env)
    
    loader = Loader(filename)
    loader.load(kernel)

    kernel.buildTransports()
    kernel.buildPassengers(1000)

    kernel.run()

    env.run(until=1000)


if __name__ == '__main__':
    seed()
    if len(argv) > 1:
        filename = argv[1]
        if os.path.exists(filename):
            mainLoading(filename)
            exit()
    main()

