import pygame, random, os
from .settings import *
vec = pygame.math.Vector2

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
bullet = pygame.sprite.Group()
map_group = pygame.sprite.Group()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = all_sprites, obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.texture = {
            0 : pygame.image.load(os.path.join(img_dir, "1.png")),
            1 : pygame.image.load(os.path.join(img_dir, "1.png")),
            2 : pygame.image.load(os.path.join(img_dir, "2.png")),
            3 : pygame.image.load(os.path.join(img_dir, "3.png")),
            4 : pygame.image.load(os.path.join(img_dir, "4.png")),
            5 : pygame.image.load(os.path.join(img_dir, "5.png")),
            6 : pygame.image.load(os.path.join(img_dir, "6.png")),
            7 : pygame.image.load(os.path.join(img_dir, "7.png")),
            8 : pygame.image.load(os.path.join(img_dir, "1.png")),
            9 : pygame.image.load(os.path.join(img_dir, "9.png")),
            10 : pygame.image.load(os.path.join(img_dir, "9.png")),
            11 : pygame.image.load(os.path.join(img_dir, "11.png")),
            12 : pygame.image.load(os.path.join(img_dir, "12.png")),
            13 : pygame.image.load(os.path.join(img_dir, "13.png")),
            14 : pygame.image.load(os.path.join(img_dir, "14.png")),
            15 : pygame.image.load(os.path.join(img_dir, "15.png")),
            16 : pygame.image.load(os.path.join(img_dir, "16.png")),
            17 : pygame.image.load(os.path.join(img_dir, "17.png")),
            18 : pygame.image.load(os.path.join(img_dir, "11.png")),
            19 : pygame.image.load(os.path.join(img_dir, "19.png")),
            20 : pygame.image.load(os.path.join(img_dir, "19.png")),
        }

        self.game = game
        self.image = random.choice(self.texture)
        self.rect = self.image.get_rect()
        #self.x, self.y = x*TILESIZE, y*TILESIZE
        self.pos = vec(random.randrange(-20*TILESIZE, DEFAULT_WIDTH), random.randrange(-10, 0))
        self.vel = vec(0, 0)
        self.acc = vec(random.uniform(-2.0, 0.2), random.uniform(0.05, 0.2))
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.vel += self.acc
        self.pos += self.vel * self.game.dt#+ 0.5 * self.acc
        self.rect.midbottom = self.pos
        if self.vel.x > 1 or self.vel.y > 1:
            self.vel.x = 1
            self.vel.y = 1
        if self.rect.top > DEFAULT_HEIGHT + 10:
            self.pos = vec(random.randrange(-20*TILESIZE, DEFAULT_WIDTH), random.randrange(-10, 0))
            self.acc = vec(random.uniform(-2.0, 0.2), random.uniform(0.05, 0.1))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = all_sprites, bullet
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join(img_dir, "bullet.png"))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, -1)
        self.last_update = pygame.time.get_ticks()

    def destroy_object(self):
        collide = pygame.sprite.spritecollide(self, obstacles, True)
        if collide:
            self.kill()

    def update(self):
        self.destroy_object()
        self.vel += self.acc
        self.pos += self.vel * self.game.dt#+ 0.5 * self.acc
        self.rect.midbottom = self.pos
        if self.rect.top < 0:
            self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.pos = vec(x, y)
    
    def update(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y