from abc import abstractmethod, ABC


class Atomic(ABC):
    def __init__(self):
        self.__changed = False

    def hasChanged(self):
        return self.__changed

    def markChange(self):
        self.__changed = True
