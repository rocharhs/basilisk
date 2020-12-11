import numpy as np
      
# Snake World  
class World:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.snakes = []
        # all position tuples
        world_pos = np.where(np.ones((rows,cols)))
        self.space = set(zip(world_pos[0], world_pos[1]))
        self.reset()

    def reset(self):
        # position food and snakes
        for snake in self.snakes:
            snake.reset(self.get_freespace())
        self.place_food()

    def get_pos(self, pos):
        # Returns a valid position, given arbitrary posistion tuple pos
        r,c = pos[0],pos[1]
        if pos[0] < 0:
            r = self.rows + pos[0]
        elif pos[0] >= self.rows:
            r = pos[0] % self.rows
        if pos[1] < 0:
            c = self.cols + pos[1]
        elif pos[1] >= self.cols:
            c = pos[1] % self.cols
        return (r,c)

    def get_freespace(self):
        # Returns a random free space cell
        free_space = self.space.copy()

        for snake in self.snakes:
            free_space -= set(snake.get_all_blocks())

        free_space = list(free_space)

        return free_space[np.random.randint(len(free_space))]

    def place_food(self):
        # puts food on a random free space cell
        self.food = self.get_freespace()

    def iterate(self):
        # move all live snakes
        ate = False
        for snake in self.snakes:
            if snake.alive:
                snake.move()
                # if this snake ate food, change food location
                if snake.head == self.food:
                    self.place_food()
                    ate = True
        return ate

    def get_color_matrix(self):
        # Returns image 3d vector representing world color matrix

        #Empty blocks are black
        room = np.zeros((self.rows,self.cols,3))

        for snake in self.snakes:
            # paint snake blocks with snake color
            for body in snake.get_all_blocks():
                room[body[0],body[1]] = snake.color

        # food is red (255,0,0)
        room[self.food[0],self.food[1]] = (255,0,0)

        return room
