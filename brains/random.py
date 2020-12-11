import numpy as np
from snake_brain import Brain

class RandomBrain(Brain):
    # A Cuckoo snake
    def __init__(self):
        super().__init__()
        self.c = 0

    def update_direction(self, world_view, snake_head, snake_color):

        return self.allowed_directions[np.random.randint(
            len(self.allowed_directions))]

    def update_brain(self, reward):
        self.c += reward