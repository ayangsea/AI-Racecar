import math

class Ray():
    def __init__(self, angle_relative_to_car, show, pixels, car):
        self.angle_relative_to_car = angle_relative_to_car
        self.show = show
        self.pixels = pixels
        self.car = car
        self.increment_distance = 1
    
    def closest_boundary_point(self):
        print("calculate distance")
        x = self.car.rect.centerx
        y = self.car.rect.centery
        print(x, y)
        track = self.car.track
        while track.pixels[round(x)][round(y)] == 1: #while it is not out of bounds
            x += self.increment_distance * math.cos(self.angle_relative_to_car - self.car.direction)
            y += self.increment_distance * math.sin(self.angle_relative_to_car - self.car.direction)
        return (x, y)