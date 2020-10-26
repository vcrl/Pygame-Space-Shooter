import pygame
from .settings import *
vec = pygame.math.Vector2

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
map_group = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0, PLAYER_GRAV)
        self.acc = vec(0, 0)
        self.state = {
            "debug_mode" : False,
            "on_ground" : False,
        }

    def collide_with_walls(self, direction):
        if direction == "x":
            collision = pygame.sprite.spritecollide(self, walls, False)
            obs_collision = pygame.sprite.spritecollide(self, obstacles, False)
            if collision:
                if self.vel.x > 0 or self.game.map.state["moving"]:
                    self.pos.x = collision[0].rect.left - self.rect.width
                if self.vel.x < 0 :
                    self.pos.x = collision[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
                self.state["on_ground"] = False
            if obs_collision:
                if self.vel.x > 0 or self.game.map.state["moving"]:
                    self.pos.x = obs_collision[0].rect.left# - self.rect.width
                if self.vel.x < 0 :
                    self.pos.x = obs_collision[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
                self.state["on_ground"] = False
        if direction == "y":
            collision = pygame.sprite.spritecollide(self, walls, False)
            obs_collision = pygame.sprite.spritecollide(self, obstacles, False)
            if collision:
                if self.vel.y > 0:
                    self.pos.y = collision[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = collision[0].rect.bottom #+ self.rect.height
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.state["on_ground"] = True
            if obs_collision:
                if self.vel.x > 0 or self.game.map.state["moving"]:
                    self.pos.x = obs_collision[0].rect.left - self.rect.width
                if self.vel.x < 0 :
                    self.pos.x = obs_collision[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
                self.state["on_ground"] = True

    def x_movement(self):
        self.acc.x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.acc.x -= PLAYER_ACCELERATION
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x += PLAYER_ACCELERATION

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel.x += self.acc.x
        self.pos.x += self.acc.x * self.game.dt
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        self.rect.x = self.pos.x
        self.collide_with_walls("x")

    def y_movement(self):
        if not self.state["on_ground"]:
            self.vel.y = PLAYER_GRAV
        else:
            self.vel.y = 0
        keys = pygame.key.get_pressed()
        if self.vel.y == 0:
            if keys[pygame.K_SPACE] or keys[pygame.K_z]:
                self.acc.y = -PLAYER_JUMP_FORCE
                self.state["on_ground"] = False
        
        self.acc.y += self.vel.y * PLAYER_FRICTION
        self.vel.y += self.acc.y
        self.pos.y += self.acc.y * self.game.dt
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.y = self.pos.y
        self.collide_with_walls("y")

    def debug_mode(self):
        if self.state["debug_mode"]:
            key = pygame.key.get_pressed()
            self.acc.y = 0
            if key[pygame.K_p]:
                self.pos.x = 0

    def update(self):
        self.collide_with_walls("x")
        self.debug_mode()
        if self.game.state != "paused":
            self.x_movement()
            #if not self.state["debug_mode"]:
            self.y_movement()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, themap, game, x, y, w, h):
        self.groups = all_sprites, obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.map = themap
        self.game = game
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.pos = vec(int(x*TILESIZE), int(y*TILESIZE))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.on_ground = False

    def collide_with_walls(self, direction):
        if direction == "x":
            collision = pygame.sprite.spritecollide(self, walls, False)
            if collision:
                if self.vel.x > 0 or self.game.map.state["moving"]:
                    self.pos.x = collision[0].rect.left - self.rect.width
                if self.vel.x < 0 :
                    self.pos.x = collision[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if direction == "y":
            collision = pygame.sprite.spritecollide(self, walls, False)
            self_collision = pygame.sprite.spritecollide(self, obstacles, False)
            if self_collision:
                self.on_ground = True
                #self.pos.y = self_collision[0].rect.top - self.rect.height
                self.vel.y = 0
                self.rect.y = self.pos.y
            if collision:
                self.on_ground = True
                self.pos.y = collision[0].rect.top - self.rect.height
                self.vel.y = 0
                self.rect.y = self.pos.y

    def y_movement(self):
        if self.on_ground:
            self.vel.y = 0
        else:
            self.vel.y = OBS_GRAV
        self.acc.y += self.vel.y
        self.pos.y += self.acc.y * self.game.dt

    def update(self):
        self.y_movement()
        self.rect.y = self.pos.y
        self.collide_with_walls("y")
        self.rect.x = self.pos.x
        self.collide_with_walls("x")

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