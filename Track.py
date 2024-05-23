from PIL import Image
import numpy
import pandas
import Const
import pygame

class Track():

    def __init__(self, track, screen, startX, startY):
        self.trackImg = track
        self.track = Image.open(track).load()
        self.np_img = numpy.array(self.track)
        self.pixels = numpy.zeros((Const.SCREEN_WIDTH, Const.SCREEN_HEIGHT))
        self.screen = screen
        self.color_checkpoint_map = {}
        self.startX = startX
        self.startY = startY

    def init_checkpoints(self, checkpoints):
        checkpointID = 1
        color = [0, 0, 255]
        for checkpoint in checkpoints:
            checkpoint.drawCheckpoint(color)
            self.color_checkpoint_map[self.screen.map_rgb(tuple(color))] = checkpointID
            color[2] -= 1
            checkpointID += 1
    
    def track_pixel_array(self):
        pixel_array = pygame.surfarray.array2d(self.screen)
        out = self.screen.map_rgb((255, 255, 255))
        for x in range(Const.SCREEN_WIDTH):
            for y in range(Const.SCREEN_HEIGHT):
                if pixel_array[x, y] == out:
                    self.pixels[x][y] = Const.OUT_OF_BOUNDS
                elif pixel_array[x, y] in self.color_checkpoint_map.keys():
                    self.pixels[x][y] = self.color_checkpoint_map[pixel_array[x, y]]






