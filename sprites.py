#Sprite Classes
import pygame
from settings import *

Vec = pygame.math.Vector2

class Bird(pygame.sprite.Sprite):
    def __init__(self, game, image_string):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load(image_string)
        self.image = pygame.transform.scale(self.image, (BIRD_SIZE))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/4, HEIGHT/4)
        self.pos = Vec(WIDTH/4, HEIGHT/4)
        self.vel = Vec(0, 0)
        self.acc = Vec(0, 0)

    def fly(self):
        #Bird fly
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            BIRD_FLY = 10
        else:
            BIRD_FLY = 5

        self.vel.y = -BIRD_FLY

    def update(self):
        self.acc = Vec(0, BIRD_GRAVITY)
        self.vel.x = BIRD_VEL_X
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -BIRD_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = BIRD_ACC

        #apply friction
        self.acc.x += self.vel.x * BIRD_FRICTION
        #Eqns of motion
        self.vel += self.acc
        self.pos += self.vel + (self.acc/2)
        #Bondary conditions
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
            self.vel.x = 0
        if self.pos.y < 0:
            self.pos.y = 0
            self.vel.y = 0
        if self.pos.y > HEIGHT:
            self.pos.x = HEIGHT
            self.vel.x = 0

        #assign position
        self.rect.midbottom = self.pos


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image_string):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_string)
        self.image = pygame.transform.scale(self.image, (w, int(h)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = True

    def de_activate(self):
        self.active = False


class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image_string):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_string)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
