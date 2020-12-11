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

