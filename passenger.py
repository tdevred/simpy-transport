class Passenger:
    def __init__(self, id_passenger, path) -> None:
        self.id = id_passenger
        self.path = path

    def __repr__(self) -> str:
        return f'Passenger {self.id}'

    def needsToLeaveNext(self):
        return self.path.needsToLeaveNext()

    def nextNode(self):
        self.path.nextNode()

    def getNode(self):
        return self.path.currentNode()