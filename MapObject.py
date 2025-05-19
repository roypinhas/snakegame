from abc import ABC, abstractmethod


class MapObject(ABC):
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass