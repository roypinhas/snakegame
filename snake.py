from config import GRID_WIDTH, GRID_HEIGHT


class Snake:
    def __init__(self, body, direction, head_img):
        self.body = body
        self.direction = direction
        self.grow_next_move = False
        self.head_img = head_img

    def move(self):
        head_x, head_y = self.body[0]
        direction_x, direction_y = self.direction.vector
        new_head = (head_x + direction_x, head_y + direction_y)
        self.body.insert(0, new_head)

        if self.grow_next_move:
            self.grow_next_move = False
        else:
            self.body.pop()

    def grow(self):
        self.grow_next_move = True

    def set_direction(self, direction):
        # we can't allow the snake to go in a reversed direction
        if tuple(-x for x in direction.vector) != self.direction.vector:
            self.direction = direction

    def check_collision(self):
        head = self.body[0]
        return (
                head in self.body[1:] or
                not (0 <= head[0] < GRID_WIDTH) or
                not (0 <= head[1] < GRID_HEIGHT)
        )

    def draw(self, screen):
        pass