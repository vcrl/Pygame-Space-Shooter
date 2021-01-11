import pygame, random, os
from .settings import *
from .sprites import all_sprites, walls, obstacles, Bullet
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0, 0)
        self.acc = vec(0, PLAYER_GRAV)
        self.state = {
            "debug_mode" : False,
            "on_ground" : False,
            "jumping" : False,
        }
        self.last_shot = 0
        self.last_hit = 0
        self.lives = 3

    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, walls, False)
        self.rect.y -= 2
        if hits:
            self.vel.y = -PLAYER_JUMP_FORCE

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.acc.x = -PLAYER_ACCELERATION
        if keys[pygame.K_d]:
            self.acc.x = PLAYER_ACCELERATION

    def collisions(self):
        # Ground collisions
        if self.vel.y > 0:
            hits = pygame.sprite.spritecollide(self, walls, False)
            if hits:
                self.pos.y = hits[0].rect.y
                self.vel.y = 0

        collide = pygame.sprite.spritecollide(self, obstacles, False)
        now = pygame.time.get_ticks()
        if now - self.last_hit > HIT_RATE:
            if collide:
                self.last_hit = now
                self.lives -= 1

    def shoot_bullet(self):
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                Bullet(self.game, self.rect.centerx, self.rect.centery)

    def is_dead(self):
        if self.lives == 0:
            self.kill()

    def update(self):
        if self.game.state != "paused":
            print(self.lives)
            self.acc = vec(0, PLAYER_GRAV)
            self.shoot_bullet()
            self.collisions()
            self.move()
            self.is_dead()
            # apply friction
            self.acc.x += self.vel.x * PLAYER_FRICTION
            
            # equations of motion
            self.vel += self.acc
            self.pos += self.vel * self.game.dt#+ 0.5 * self.acc
            self.rect.midbottom = self.pos