import pygame
import os

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 600

# loading the images
BIRDS = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(
    os.path.join("assets", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird3.png")))]
BASE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("assets", "land.png")))
PIPE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("assets", "pipe.png")))
BACKGROUND = pygame.transform.scale2x(
    pygame.image.load(os.path.join("assets", "bg.png")))


class Bird:
    bird_images = BIRDS

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.tick_count = 0
        self.height = self.y
        self.tilt = 0
        self.img_count = 0
        self.img = self.bird_images[0]

    def move(self):
        self.tick_count += 1
        # displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2


    def jump(self):
        self.vel = -10 # -ve to go up
        self.tick_count = 0
        self.height = self.y
