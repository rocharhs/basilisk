import numpy as np


# A Treacherous Snake!
class Snake:


    def __init__(
        self, 
        world_view, # How the snake sees the world
        i=0,j=0, # snake initial position
        color=(0,255,0) # snake block color and ID
        ): 

        self.head = (i,j)
        self.body = []
        self.color = color
        self.world_view = world_view

        self.directions = {
                'DOWN':(1,0),
                'UP':(-1,0),
                'RIGHT':(0,1),
                'LEFT':(0,-1)
                }

        self.dir = 'RIGHT'
        self.alive = True
        self.brain = None

        self.allowed_colors = [
            (0,0,0), #empty
            (255,0,0) #food
        ]

    # Add brainz
    def set_brain(self, brain):
        self.brain = brain

    # Ouroboros
    def reset(self, pos):
        self.head = pos
        self.body = []
        self.dir = 'RIGHT'
        self.alive = True

    # Check if new direction is valid and change to it
    def change_direction(self, direction):
        next_direction = np.array(
                self.directions[direction]) 

        current_direction = np.array(
                self.directions[self.dir])

        if np.any(current_direction != -next_direction):
            self.dir = direction

    # Returns all snake blocks
    def get_all_blocks(self):
        return [self.head] + self.body

    def move(self):
        # If it has a brain, use it
        if self.brain is not None:
            # try to change to brainy direction
            self.change_direction(
                self.brain.update_direction(
                    self.world_view,
                    self.head,
                    self.color))
            
        # Establishes current direction
        new_direction = self.directions[self.dir]

        # Determine future head position
        new_head = self.world_view.get_pos(
                np.array(self.head) + 
                np.array(new_direction))

        # Increase body size
        self.body = self.get_all_blocks()

        # If didn't eat this round
        if not self.world_view.get_food() == new_head:
            # loses weight
            self.body.pop()
        # If it did eat
        elif self.brain is not None:
            # tells the brain it is delicious
            self.brain.update_brain(1)

        # recover world view, assuming it is a block map
        block_map = self.world_view.get_view()

        # if the future head is in collision with other snakes, it dies
        if not tuple(block_map[new_head[0], new_head[1]]) in self.allowed_colors:
            self.alive = False
            if self.brain is not None:
                # if it dies, punish the brain
                self.brain.update_brain(-1)

        # I prefer to be this walking metamorphosis
        self.head = new_head