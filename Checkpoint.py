import pygame

class Checkpoint():
    def __init__(self, p1, p2, screen):
        self.p1 = p1
        self.p2 = p2
        self.screen = screen
        #self.id = id
        self.points = []

    def drawCheckpoint(self, color):
        pygame.draw.line(self.screen, color, list(self.p1), list(self.p2), 15)


