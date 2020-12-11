import pygame
import numpy as np

import snake_world
import snake_logic
import snake_brain
from brains.greedy import GreedyBrain
from brains.random import RandomBrain
import os 

# Center Screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

if __name__ == '__main__':

    # load music
    # pygame.mixer.pre_init(44100,-16,2,2048)

    # Initialize
    pygame.init()
    pygame.display.set_caption('Hydra')

    # load eating sound
    eat_sound = pygame.mixer.Sound('rsc/sound/eat.wav')
    death_sound = pygame.mixer.Sound('rsc/sound/die.wav')
    eat_sound.set_volume(0.3)
    death_sound.set_volume(0.3)

    #load music
    #### Removed music to prevent copyright issues :(

    # pygame.mixer.music.load('rsc/music/memo.mp3')
    # pygame.mixer.music.set_volume(0.3)
    # pygame.mixer.music.play(loops=-1)

    # Text Font
    font = pygame.font.Font('freesansbold.ttf', 32) 

    # Grid World
    GR, GC = 20,20
    world = snake_world.World(GR,GC)

    # First Snake
    snakeA = snake_logic.Snake(
        snake_brain.WorldView(world),
        color=(0,255,0))

    # Add Greedy Brain to Snake
    snakeA.set_brain(RandomBrain())

    # Lylith, Second Snake
    snakeB = snake_logic.Snake(
        snake_brain.WorldView(world),
        color=(255,0,255))

    snakeB.set_brain(GreedyBrain())

    # Lupin, the Third
    snakeC = snake_logic.Snake(
        snake_brain.WorldView(world),
        color=(0,255,255))
    snakeC.set_brain(GreedyBrain())

    snakeD = snake_logic.Snake(
        snake_brain.WorldView(world),
        color=(255,127,0))

    snakeD.set_brain(RandomBrain())
    
    # Throws snakes into the world
    world.snakes.append(snakeA)
    world.snakes.append(snakeB)
    world.snakes.append(snakeC)
    world.snakes.append(snakeD)

    # Reposition snakes in the world
    world.reset()

    # Game Screen Size
    WIDTH = 520
    HEIGHT = 520

    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    clock = pygame.time.Clock()
    FPS = 150

    running = True

    ###### Utility functions for game state management

    # check if there is at least a snake alive
    is_valid = lambda snake_list:np.any([x.alive for x in snake_list])

    # returns the size of every snake
    snakes_length = lambda snake_list:[len(x.body) for x in snake_list]

    # winner snake id
    get_winner = lambda snake_list:np.argmax(snakes_length(snake_list))

    # Killed snakes list
    funeral = [False]*len(world.snakes)
    score = [0]*len(world.snakes)

    # Initial Direction
    new_dir = 'RIGHT'
    score_positions = []
    for i in range(len(world.snakes)):
        score_positions.append((0,i*40))
    slow_motion = False


    while running:

        if slow_motion:
            clock.tick(FPS//10)
        else:
            clock.tick(FPS)

        # If there is at least one snake alive
        if is_valid(world.snakes):
            # executes a step and checks if apple was eaten
            ate = world.iterate()

            # if apple was eaten play sound
            if ate and slow_motion:
                eat_sound.play()

        else:
            # If everybody died, get winner
            winner = get_winner(world.snakes)
            # increase winners score
            score[winner] += 1
            world.reset()
            funeral = [False]*len(world.snakes)
        
        # Check if a new snake died
        for i in range(len(world.snakes)):
            # if a snake dies, give it a proper funeral
            if not world.snakes[i].alive and not funeral[i]:
                if slow_motion:
                    death_sound.play()
                funeral[i] = True

        # Check keyboard events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Allow impatiant watchers to reset the game
                elif event.key == pygame.K_SPACE:
                    world.reset()
                    funeral = [False]*len(world.snakes)
                elif event.key == pygame.K_s:
                    slow_motion = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    slow_motion = False


        #### DRAW ####
        screen.fill((0,0,0))

        # Numa folha qualquer
        background = pygame.Surface((GC,GR))

        # Eu desenho o mundo
        pygame.surfarray.blit_array(background, world.get_color_matrix().transpose(1,0,2))

        # E estico a folha pra preencher a tela
        background = pygame.transform.scale(background, screen.get_size())

        # E emolduro a tela no monitor
        screen.blit(background, (0,0))

        # For each snake 
        for i in range(len(world.snakes)):
            # draws snake score if its respective color
            text = font.render(
                    str(score[i]), 
                    True, world.snakes[i].color
                    , (0,0,0))

            # Position text in respective corner
            textRect = text.get_rect()
            screen.blit(text, score_positions[i])

        # update screen
        pygame.display.flip()

    pygame.quit()
