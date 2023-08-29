import random
import pygame
import os
import neat

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

pygame.font.init()
FONT = pygame.font.SysFont('Arial', 30)
generation = 0
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

def draw_window(win, birds, pipes, base, score, gen, alive):
    win.blit(BACKGROUND, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    text = FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WINDOW_WIDTH - 10 - text.get_width(), 10))
    gen_text = FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(gen_text, (10,10))
    alive_text = FONT.render("Alive: " + str(alive), 1, (255,255,255))
    win.blit(alive_text, (10, gen_text.get_height() + 5))
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()

def eval_genomes(genomes, config):
    global generation
    birds = []
    networks = []
    genome_list = []
    base = Base(730)
    pipes = [Pipe(600)]

    for _, genome in genomes:
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        birds.append((Bird(230,350)))
        genome_list.append(genome)
        genome.fitness = 0

    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    run = True
    score = 0
    generation+=1
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        alive = len(birds)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        rem  = []
        add_pipe = False
        pipe_no = 0

        if(len(birds) <= 0):
            break

        if(len(birds) > 0 and len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()):
            pipe_no = 1

        for x, bird in enumerate(birds):
            bird.move()
            genome_list[x].fitness += 1

            output = networks[x].activate((bird.y, abs(bird.y - pipes[pipe_no].height), abs(bird.y - pipes[pipe_no].bottom)))
            if output[0] > 0.5:
                bird.jump()

        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird, win):
                    genome_list[x].fitness -= 1
                    birds.pop(x)
                    networks.pop(x)
                    genome_list.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            pipe.move()
        
        if add_pipe:
            score += 1
            for genome in genome_list:
                genome.fitness += 5
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)

        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                networks.pop(x)
                genome_list.pop(x)

        if score > 50:
            break
        base.move()
        draw_window(win , birds, pipes, base, score, generation, alive)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat-config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(eval_genomes, 50)
