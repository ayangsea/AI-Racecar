from numpy import Infinity
from Ray import Ray
import pygame
import math
import Const
from Brain import Brain
import time

class Car(pygame.sprite.Sprite):
    def __init__(self, screen, track, showRays, brain=None):
        super(Car, self).__init__()
        self.img = pygame.image.load(Const.CAR_IMG)
        self.surf = self.img.convert()
        self.rect = self.surf.get_rect()
        self.track = track
        self.direction = self.track.startAngle #starting angle in radians (pointing right)
        self.speed = 0 
        self.x = self.track.startX
        self.y = self.track.startY
        self.screen = screen
        self.score = 0
        self.fitness = 0
        self.showRays = showRays
        self.controls = {'accelerate': 0, 'decelerate': 0, 'turn_left': 0, 'turn_right': 0}
        self.checkpoints_reached = []
        self.num_checkpoints_reached = 0
        self.start_time = time.time()
        self.time_since_last_checkpoint = 0
        self.last_checkpoint_time = self.start_time
        if brain:
            self.brain = brain.copy()
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
            self.speed = max(min(self.speed + Const.CAR_ACCEL, Const.CAR_MAX_SPEED), 0)
        if self.controls['decelerate']:
            self.speed = max(min(self.speed - Const.CAR_ACCEL, Const.CAR_MAX_SPEED), 0)
        if self.controls['turn_left']:
            self.direction += Const.CAR_ROTATE_SPEED
        if self.controls['turn_right']:
            self.direction -= Const.CAR_ROTATE_SPEED
        dx = self.speed * math.cos(self.direction)
        dy = self.speed * -math.sin(self.direction)
        self.x += dx
        self.y += dy
        self.rect.move_ip(dx, dy)

    def check_kill_conditions(self, generation, savedCars):

        #track bounds
        if self.track.pixels[self.rect.centerx][self.rect.centery] == Const.OUT_OF_BOUNDS:
            self.speed = 0
            self.kill(generation, savedCars)
            return

        #going backwards
        if (len(self.checkpoints_reached) == 0 and self.track.pixels[self.rect.centerx][self.rect.centery] == self.track.num_checkpoints + 1):
            self.kill(generation, savedCars)
            return
        elif len(self.checkpoints_reached) > 0 and self.track.pixels[self.rect.centerx][self.rect.centery] == self.checkpoints_reached[len(self.checkpoints_reached) - 1] - 1:
            self.kill(generation, savedCars)
            return
        
        #time between checkpoints
        if self.time_since_last_checkpoint > Const.CHECKPOINT_TIMEOUT:
            self.kill(generation, savedCars)
            return

        #max generation time
        if time.time() - self.start_time > Const.GENERATION_TIMEOUT:
            self.kill(generation, savedCars)
            return
    
    def update_checkpoints(self):
        pixel_value = self.track.pixels[self.rect.centerx][self.rect.centery]
        if pixel_value >= 1 and not pixel_value in self.checkpoints_reached:
            #print("new checkpoints")
            self.checkpoints_reached.append(pixel_value)
            self.time_since_last_checkpoint = 0
            self.last_checkpoint_time = time.time()
            self.num_checkpoints_reached += 1
        if pixel_value == 1 and len(self.checkpoints_reached) > 1:
            self.checkpoints_reached = [1]
            self.num_checkpoints_reached += 1
        self.time_since_last_checkpoint = time.time() - self.last_checkpoint_time
        
    
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
        #print(outputs)
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

    def set_score(self):
        time_alive = time.time() - self.start_time
        self.score = self.num_checkpoints_reached * self.num_checkpoints_reached
        if self.x == self.track.startX and self.y == self.track.startY:
            self.score = 0

    def kill(self, generation, savedCars):
        generation.remove(self)
        self.set_score()
        savedCars.append(self)

    def update(self, pressed_keys, generation, savedCars):
        self.update_controls(pressed_keys)
        self.think()
        self.move()
        self.rotate()
        self.check_kill_conditions(generation, savedCars)
        self.update_checkpoints()
        if self.showRays:
            self.displayRays()
       
        


        
