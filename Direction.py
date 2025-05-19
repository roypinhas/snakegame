from enum import Enum


class Direction(Enum):
    UP = ((0, -1), 90)
    DOWN = ((0, 1), 270)
    LEFT = ((-1, 0), 180)
    RIGHT = ((1, 0), 0)

    @property
    def vector(self):
        return self.value[0]

    @property
    def rotation(self):
        return self.value[1]