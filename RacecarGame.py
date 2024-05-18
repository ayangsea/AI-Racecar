import pygame
from Car import Car
import time
import Const
from Track import Track

pygame.init()

TRACKS = [Const.TRACK1]

screen = pygame.display.set_mode([Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT])
 
running = True
track = pygame.image.load(TRACKS[0])
clock = pygame.time.Clock()

track1 = Track(Const.TRACK1)
car = Car(Const.CAR_MAX_SPEED, Const.CAR_ROTATE_SPEED, Const.CAR_ACCEL, screen, track1)

while running:
    clock.tick(Const.FPS) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    screen.blit(track, (0, 0))
    pressed_keys = pygame.key.get_pressed()
    car.update(pressed_keys, screen)

    pygame.display.flip()
    time.sleep(0.005)

pygame.quit()