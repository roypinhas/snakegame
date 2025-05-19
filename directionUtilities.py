from Direction import Direction


def get_dir(pos1, pos2):
    """Return direction vector from pos1 to pos2."""
    return pos2[0] - pos1[0], pos2[1] - pos1[1]


def vector_to_direction(vector):
    for direction in Direction:
        if direction.vector == vector:
            return direction
    return None