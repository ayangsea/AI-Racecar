import pygame
from Car import Car
import Const
from Track import Track
from Brain import Brain
import pandas
from Checkpoint import Checkpoint

pygame.init()

TRACKS = [Const.TRACK1]

screen = pygame.display.set_mode([Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT])
 
running = True
track = pygame.image.load(TRACKS[0])
clock = pygame.time.Clock()

track1 = Track(Const.TRACK1, screen)
cars = [Car(Const.CAR_MAX_SPEED, Const.CAR_ROTATE_SPEED, Const.CAR_ACCEL, screen, track1, True) for i in range(Const.NUM_CARS_PER_GENERATION)]
screen.blit(track, (0, 0))
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
    
    screen.blit(track, (0, 0))
    pressed_keys = pygame.key.get_pressed()
    for car in cars:
        car.update(pressed_keys)
    
    for checkpoint in checkpoints:
        checkpoint.drawCheckpoint((0, 0, 255))


    pygame.display.flip()

pygame.quit()