import random
import pygame
import os

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 500

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
    MAX_ROTATION = 20
    ROTATION_VEL = 20
    ANIMATION_TIME = 5

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
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2 # ut + 1/2 at^2, a = 3
        
        if displacement >= 15:
            # stop from moving too much
            displacement = 15
        
        if displacement < 0:
            displacement -= 3
        self.y += displacement
        
        if displacement < 0 or self.y < self.height + 50:
            # tilt the bird upwards
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VEL

    def jump(self):
        self.vel = -10 # -ve to go up
        self.tick_count = 0
        self.height = self.y

    def draw(self, win):
        self.img_count += 1

        # flaps the bird
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.bird_images[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.bird_images[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.bird_images[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.bird_images[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.bird_images[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.bird_images[1]
            self.img_count = self.ANIMATION_TIME * 2
        
        rotate_img = pygame.transform.rotate(self.img, self.tilt)
        rect = rotate_img.get_rect(center= self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotate_img, rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Base:
    VEL = 5
    WIDTH = BASE.get_width()
    IMG = BASE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):

        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):

        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


class Pipe():
    DIFF = 200
    VEL = 5
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.diff = 100
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE, False, True)
        self.PIPE_BOTTOM = PIPE

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.DIFF

    def move(self):


        self.x -= self.VEL

    def draw(self, win):

        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird, win):

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False

def draw_window(win, bird):
    win.blit(BACKGROUND, (0,0))
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window(win , bird)
        bird.move()
    pygame.quit()
    quit()

main()