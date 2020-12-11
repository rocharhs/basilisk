import numpy as np

# World View
class WorldView:

    # A watered down, partial and obscure version of 
    # the REAL world - PLATO
    def __init__(self, world):

        self.world = world

    # Knows where the food is
    def get_food(self):
        return self.world.food

    # Knows how to get well positioned
    def get_pos(self, pos):
        return self.world.get_pos(pos)

    # Knows the color of each block on the map
    def get_view(self):
        return self.world.get_color_matrix()

# Snake Brain
class Brain:


    def __init__(self):
        # Possible directions returned by update_direction
        self.allowed_directions = [
        'LEFT','RIGHT','UP','DOWN']

    # Snakes decide how to move
    # based on a world_view, head position and color
    def update_direction(self, world_view, snake_head, snake_color):
        pass

    # Snake feedback
    def update_brain(self, reward):
        pass


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


class GreedyBrain(Brain):
    # Loves apples and gardens
    def __init__(self):
        super().__init__()

    def update_direction(self, world_view, snake_head, snake_color):

        # print('food: ', world_view.get_food(), '; pos: ', snake_head)
        desired_dir = np.array(world_view.get_food())-np.array(snake_head)

        #vertical priority [rows]
        if np.abs(desired_dir[0]) > np.abs(desired_dir[1]):
            if desired_dir[0] > 0: #must add rows
                return 'DOWN'
            else:
                return 'UP'
        else:
            if desired_dir[1] > 0:
                return 'RIGHT'
            else:
                return 'LEFT'
