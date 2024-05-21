import math
import Const

class Ray():
    def __init__(self, angle_relative_to_car, show, pixels, car):
        self.angle_relative_to_car = angle_relative_to_car
        self.show = show
        self.pixels = pixels
        self.car = car
        self.increment_distance = 1
    
    def closest_boundary_point(self):
        x = self.car.rect.centerx
        y = self.car.rect.centery
        track = self.car.track
        while not track.pixels[round(x)][round(y)] == Const.OUT_OF_BOUNDS: #while it is not out of bounds
            x += self.increment_distance * math.cos(self.angle_relative_to_car - self.car.direction)
            y += self.increment_distance * math.sin(self.angle_relative_to_car - self.car.direction)
        return (x, y)