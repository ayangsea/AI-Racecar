import pygame
from Car import Car
import Const
from Track import Track
from Brain import Brain

pygame.init()

TRACKS = [Const.TRACK1]

screen = pygame.display.set_mode([Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT])
 
running = True
track = pygame.image.load(TRACKS[0])
clock = pygame.time.Clock()

track1 = Track(Const.TRACK1)
#car = Car(Const.CAR_MAX_SPEED, Const.CAR_ROTATE_SPEED, Const.CAR_ACCEL, screen, track1, True)
cars = [Car(Const.CAR_MAX_SPEED, Const.CAR_ROTATE_SPEED, Const.CAR_ACCEL, screen, track1, True) for i in range(Const.NUM_CARS_PER_GENERATION)]

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

    pygame.display.flip()

pygame.quit()