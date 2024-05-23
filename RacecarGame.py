import pygame
from Car import Car
import Const
from Track import Track
from Brain import Brain
import pandas
import Genetic
import time
from Checkpoint import Checkpoint

#Global Variabls
SHOW_RAYS = False
SHOW_CHECKPOINTS = True

#Init Pygame
pygame.init()
screen = pygame.display.set_mode([Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT])
clock = pygame.time.Clock()
running = True

# #Track Images
track1Img = pygame.image.load(Const.TRACK1_IMG)
track2Img = pygame.image.load(Const.TRACK2_IMG)
track3Img = pygame.image.load(Const.TRACK3_IMG)
trackImgs = [track1Img, track2Img, track3Img]

#Track objects
track1 = Track(Const.TRACK1_IMG, screen, Const.TRACK1_START_X, Const.TRACK1_START_Y, Const.TRACK1_START_ANGLE, Const.NUM_CHECKPOINT1_POINTS)
track2 = Track(Const.TRACK2_IMG, screen, Const.TRACK2_START_X, Const.TRACK2_START_Y, Const.TRACK2_START_ANGLE, Const.NUM_CHECKPOINT2_POINTS)
track3 = Track(Const.TRACK3_IMG, screen, Const.TRACK3_START_X, Const.TRACK3_START_Y, Const.TRACK3_START_ANGLE, Const.NUM_CHECKPOINT3_POINTS)
tracks = [track1, track2, track3]

#Init Checkpoints
checkpoints1 = [Checkpoint(point[0], point[1], screen) for point in Const.CHECKPOINT1_POINTS]
checkpoints2 = [Checkpoint(point[0], point[1], screen) for point in Const.CHECKPOINT2_POINTS]
checkpoints3 = [Checkpoint(point[0], point[1], screen) for point in Const.CHECKPOINT3_POINTS]
checkpoints = [checkpoints1, checkpoints2, checkpoints3]

screen.blit(track1Img, (0, 0))
track1.init_checkpoints(checkpoints1)
track1.track_pixel_array()
screen.blit(track2Img, (0, 0))
track2.init_checkpoints(checkpoints2)
track2.track_pixel_array()
screen.blit(track3Img, (0, 0))
track3.init_checkpoints(checkpoints3)
track3.track_pixel_array()

#Init generations
generation = [Car(screen, track1, SHOW_RAYS) for i in range(Const.NUM_CARS_PER_GENERATION)]
generation_num = 0
savedCars = []
    
pygame.display.flip()
while running:
    clock.tick(Const.FPS) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    screen.blit(trackImgs[generation_num % Const.NUM_TRACKS], (0, 0))
    pressed_keys = pygame.key.get_pressed()
    if len(generation) == 0:
        generation_num += 1
        generation = Genetic.next_generation(generation, savedCars, screen, tracks[generation_num % Const.NUM_TRACKS])
        savedCars = []

    if SHOW_CHECKPOINTS:     
        for checkpoint in checkpoints[generation_num % Const.NUM_TRACKS]:
            checkpoint.drawCheckpoint((0, 0, 255))

    for car in generation:
        car.update(pressed_keys, generation, savedCars)
    
    pygame.display.flip()

pygame.quit()