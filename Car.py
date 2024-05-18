import pygame
import math
import Const

class Car(pygame.sprite.Sprite):
    def __init__(self, max_speed, rotate_speed, screen):
        super(Car, self).__init__()
        self.img = pygame.image.load(Const.CAR_IMG)
        self.surf = self.img.convert()
        self.rect = self.surf.get_rect()

        #self.x = RacecarGame.CAR_START_X #starting x coord
        #self.y = RacecarGame.CAR_START_Y #starting y coord
        self.direction = 0 #starting angle in radians (pointing right)
        self.max_speed = max_speed
        self.speed = 0 
        self.dt = 0.1
        self.x = Const.CAR_START_X
        self.y = Const.CAR_START_Y
        self.screen = screen
        self.rotate_speed = rotate_speed
        self.controls = {'accelerate': 0, 'decelerate': 0, 'turn_left': 0, 'turn_right': 0}

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

    def move(self):
        if self.controls['accelerate'] == 1:
            self.speed = min(self.speed + 1, self.max_speed)
        if self.controls['decelerate']:
            self.speed = min(self.speed - 1, self.max_speed)
        if self.controls['turn_left']:
            self.direction += self.rotate_speed
        if self.controls['turn_right']:
            self.direction -= self.rotate_speed
        dx = self.speed * self.dt * math.cos(self.direction)
        dy = self.speed * self.dt * -math.sin(self.direction)
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
        print(self.x)
    
    def rotate(self):
        rotated_image = pygame.transform.rotate(self.img, self.direction * 180 / math.pi)
        self.rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        self.screen.blit(rotated_image, self.rect.topleft)

    def update(self, pressed_keys, screen):
        self.update_controls(pressed_keys)
        self.move()
        self.rotate()
        self.check_bounds()
        
