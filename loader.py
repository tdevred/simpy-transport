from line import Line
from kernel import Kernel
import json

class Loader:

    def __init__(self, filename:str) -> None:
        self.filename = filename

    def load(self, kernel:Kernel):
        with open(self.filename, 'r') as file:
            data = json.load(file)

        self.loadSubway(data, kernel)
        self.loadBus(data, kernel)
        self.loadInterconnections(data, kernel)

    def loadSubway(self, data, kernel):
        if 'subway' in data:
            train_capacity = data['subway']['capacity']
            for line in data['subway']['lines']:
                name = line['name']
                transport_count = line['train number']
                stations = line['stations']
                durations = line['durations']

                l = Line(name, transport_count, train_capacity)

                l.addNode(stations[0])

                for node_name, duration in zip(stations[1:], durations):
                    l.addNode(node_name, duration)

                kernel.addLine(l)
            if 'connections' in data['subway']:
                for conn in data['subway']['connections']:
                    s1, s2 = conn['connection']
                    s1, s2 = f'{s1["line"]}_{s1["station"]}', f'{s2["line"]}_{s2["station"]}'
                    duration = conn['duration']
                    kernel.addInterconnection(s1, s2, duration)

    def loadBus(self, data, kernel):
        if 'bus' in data:
            bus_capacity = data['bus']['capacity']
            for line in data['bus']['lines']:
                name = line['name']
                transport_count = line['bus number']
                stops = line['stops']
                durations = line['durations']

                l = Line(name, transport_count, bus_capacity)

                l.addNode(stops[0])

                for node_name, duration in zip(stops[1:], durations):
                    l.addNode(node_name, duration)

                kernel.addLine(l)
            if 'connections' in data['bus']:
                for conn in data['bus']['connections']:
                    s1, s2 = conn['connection']
                    s1, s2 = f'{s1["line"]}_{s1["stop"]}', f'{s2["line"]}_{s2["stop"]}'
                    duration = conn['duration']
                    kernel.addInterconnection(s1, s2, duration)

    def loadInterconnections(self, data, kernel):
        if 'interconnections' in data:
            for conn in data['interconnections']:
                s1 = conn['subway']
                s2 = conn['bus']
                s1 = f'{s1["line"]}_{s1["station"]}'
                s2 = f'{s2["line"]}_{s2["stop"]}'

                duration = conn['duration']
                kernel.addInterconnection(s1, s2, duration)