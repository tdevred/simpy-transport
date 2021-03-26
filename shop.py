from abc import ABC, abstractmethod
from passenger import Passenger
import simpy

take_duration = 1
sell_duration = 10


class Shop(ABC):

    def __init__(self, env) -> None:
        self.env = env
    
    @abstractmethod
    def run(self, passenger: Passenger):
        raise NotImplemented

    def action(self, passenger):
        yield self.env.process(self.run(passenger))
        print(f'{passenger!r} {self.__class__.ACTION} at {passenger.getNode()}')


class BoutiqueSouvenirs(Shop):
    ACTION = 'bought a souvenir'

    def __init__(self, env) -> None:
        super().__init__(env)
        self.sellers = simpy.Resource(env, capacity=1)

    def run(self, passenger: Passenger):
        with self.sellers.request() as request:
            yield request
            yield self.env.timeout(sell_duration)

class Sandwicherie(Shop):
    ACTION = 'took a sandwich'

    def __init__(self, env) -> None:
        super().__init__(env)
        self.sellers = simpy.Resource(env, capacity=2)

    def run(self, passenger: Passenger):
        with self.sellers.request() as request:
            yield request
            yield self.env.timeout(sell_duration)
