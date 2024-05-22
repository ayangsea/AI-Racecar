import pygame
from Car import Car
import Const
from Track import Track
from Brain import Brain
import pandas
import Genetic
from Checkpoint import Checkpoint

pygame.init()

TRACKS = [Const.TRACK1]

screen = pygame.display.set_mode([Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT])
 
running = True
trackImg = pygame.image.load(TRACKS[0])
clock = pygame.time.Clock()

track1 = Track(Const.TRACK1, screen)
generation = [Car(Const.CAR_MAX_SPEED, Const.CAR_ROTATE_SPEED, Const.CAR_ACCEL, screen, track1, True) for i in range(Const.NUM_CARS_PER_GENERATION)]
savedCars = []
screen.blit(trackImg, (0, 0))
checkpoints = [Checkpoint(point[0], point[1], screen) for point in Const.CHECKPOINT1_POINTS]
track1.init_checkpoints(checkpoints)
track1.track_pixel_array()
pygame.display.flip()
    
while running:
    clock.tick(Const.FPS) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    screen.blit(trackImg, (0, 0))
    pressed_keys = pygame.key.get_pressed()
    if len(generation) == 0:
        generation = Genetic.next_generation(generation, savedCars, screen, track1)
        savedCars = []

    for car in generation:
        car.update(pressed_keys, generation, savedCars)
    
    for checkpoint in checkpoints:
        checkpoint.drawCheckpoint((0, 0, 255))


    pygame.display.flip()

pygame.quit()