import numpy as np
from snake_brain import Brain

class GreedyBrain(Brain):
    # Loves apples and gardens
    def __init__(self):
        super().__init__()

    def update_direction(self, world_view, snake_head, snake_color):

        food_pos = np.array(world_view.get_food())
        snake_pos = np.array(snake_head)

        desired_dir = food_pos - snake_pos
        row_dir = desired_dir[0]
        col_dir = desired_dir[1]

        #vertical priority [rows]
        if np.abs(row_dir) > np.abs(col_dir):
            if row_dir > 0: #must add rows
                return 'DOWN'
            else:
                return 'UP'
        else:
            if col_dir > 0:
                return 'RIGHT'
            else:
                return 'LEFT'
