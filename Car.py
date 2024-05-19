from numpy import Infinity
from Ray import Ray
import pygame
import math
import Const
from Brain import Brain

class Car(pygame.sprite.Sprite):
    def __init__(self, max_speed, rotate_speed, accel, screen, track, showRays, brain=None):
        super(Car, self).__init__()
        self.img = pygame.image.load(Const.CAR_IMG)
        self.surf = self.img.convert()
        self.rect = self.surf.get_rect()
        self.accel = accel
        self.direction = 0 #starting angle in radians (pointing right)
        self.max_speed = max_speed
        self.speed = 0 
        self.x = Const.CAR_START_X
        self.y = Const.CAR_START_Y
        self.screen = screen
        self.rotate_speed = rotate_speed
        self.track = track
        self.showRays = showRays
        self.controls = {'accelerate': 0, 'decelerate': 0, 'turn_left': 0, 'turn_right': 0}
        if brain:
            self.brain = brain
        else:
            self.brain = Brain(Const.BRAIN_INPUT_NODES, Const.BRAIN_HIDDEN_NODES, Const.BRAIN_OUTPUT_NODES)
        self.rays = [Ray(angle, True, self.track.pixels, self) for angle in Const.RAY_ANGLES]

    def update_controls(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.controls['accelerate'] = 1
        else:
            self.controls['accelerate'] = 0
        if pressed_keys[pygame.K_DOWN]:
            self.controls['decelerate'] = 1
        else:
            self.controls['decelerate'] = 0
        if pressed_keys[pygame.K_LEFT]:
            self.controls['turn_left'] = 1
        else:
            self.controls['turn_left'] = 0
        if pressed_keys[pygame.K_RIGHT]:
            self.controls['turn_right'] = 1
        else:
            self.controls['turn_right'] = 0

    def reset_controls(self):
        self.controls['accelerate'] = 0
        self.controls['decelerate'] = 0
        self.controls['turn_left'] = 0
        self.controls['turn_right'] = 0


    def move(self):
        if self.controls['accelerate'] == 1:
            self.speed = max(min(self.speed + self.accel, self.max_speed), -Const.CAR_MAX_SPEED)
        if self.controls['decelerate']:
            self.speed = max(min(self.speed - self.accel, self.max_speed), -Const.CAR_MAX_SPEED)
        if self.controls['turn_left']:
            self.direction += self.rotate_speed
        if self.controls['turn_right']:
            self.direction -= self.rotate_speed
        dx = self.speed * math.cos(self.direction)
        dy = self.speed * -math.sin(self.direction)
        self.x += dx
        self.y += dy
        self.rect.move_ip(dx, dy)

    def check_bounds(self):
        if self.x < 0:
            self.x = 0
        if self.x > Const.SCREEN_WIDTH:
            self.x = Const.SCREEN_WIDTH
        if self.y <= 0:
            self.y = 0
        if self.y >= Const.SCREEN_HEIGHT:
            self.y = Const.SCREEN_HEIGHT
        if self.track.pixels[self.rect.centerx][self.rect.centery] == 0:
            print('out of bounds')
            self.speed = 0
    
    def rotate(self):
        rotated_image = pygame.transform.rotate(self.img, self.direction * 180 / math.pi)
        self.rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        self.screen.blit(rotated_image, self.rect.topleft)

    def displayRays(self):
        for ray in self.rays:
            pygame.draw.line(self.screen, (0, 255, 0), list(ray.closest_boundary_point()), [self.rect.centerx, self.rect.centery], 3)
    
    def think(self):
        carPoint = (self.x, self.y)
        inputs = [self.distance(carPoint, ray.closest_boundary_point()) / Const.SCREEN_HEIGHT for ray in self.rays]
        outputs = self.brain.forward(inputs)
        print(outputs)
        maxIndex = 0
        maxValue = -Infinity
        for i in range(4):
            if outputs[i] > maxValue:
                maxIndex = i
                maxValue = outputs[i]
        
        if maxIndex == 0:
            self.controls['accelerate'] = 1
        elif maxIndex == 1:
            self.controls['decelerate'] = 1
        elif maxIndex == 2:
            self.controls['turn_left'] = 1
        elif maxIndex == 3:
            self.controls['turn_right'] = 1

    def distance(self, p1, p2):
        return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))


    def update(self, pressed_keys):
        self.update_controls(pressed_keys)
        self.think()
        self.move()
        self.rotate()
        self.check_bounds()
        if self.showRays:
            self.displayRays()


        