import pygame
from .settings import *
vec = pygame.math.Vector2

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
map_group = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, PLAYER_GRAV)
        self.state = {
            "debug_mode" : False,
            "on_ground" : True,
        }

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
            if collision:
                if self.vel.y > 0:
                    self.pos.y = collision[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = collision[0].rect.bottom #+ self.rect.height
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.state["on_ground"] = True

    def x_movement(self):
        self.acc.x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.acc.x -= PLAYER_ACCELERATION
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x += PLAYER_ACCELERATION

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel.x += self.acc.x * self.game.dt
        if self.vel.x >= 5: 
            self.vel.x = 5
        self.pos.x += self.vel.x * self.game.dt + (self.acc.x * 0.5) * ((self.game.dt * self.game.dt))
        self.rect.x = self.pos.x
        self.collide_with_walls("x")

    def y_movement(self):
        if not self.state["debug_mode"]:
            self.acc.y = PLAYER_GRAV
        else:
            self.acc.y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.acc.y = -PLAYER_ACCELERATION
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.acc.y = PLAYER_ACCELERATION
        
        self.acc.y += self.vel.y * PLAYER_FRICTION
        self.vel.y += self.acc.y * self.game.dt
        self.pos.y += self.vel.y * self.game.dt + (self.acc.y * 0.5) * ((self.game.dt * self.game.dt))
        self.rect.y = self.pos.y
        self.collide_with_walls("y")

    def player_jump(self):
        keys = pygame.key.get_pressed()
        if self.state["on_ground"]:
            if keys[pygame.K_SPACE]:
                self.vel.y = PLAYER_JUMP_FORCE
                self.state["on_ground"] = False

    def debug_mode(self):
        if self.state["debug_mode"]:
            key = pygame.key.get_pressed()
            self.acc.y = 0
            if key[pygame.K_p]:
                self.pos.x = 0

    def getrect(self):
        return self.rect

    def update(self):
        self.collide_with_walls("x")
        self.debug_mode()
        if self.game.state != "paused":
            self.x_movement()
            #if not self.state["debug_mode"]:
            self.y_movement()

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