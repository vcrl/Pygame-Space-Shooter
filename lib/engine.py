import pygame, sys, os, random
from .sprites import all_sprites, map_group, Obstacles
from .player import Player
from .menu import Pause
from .map import TiledMap_Manager
from .settings import *

class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
        pygame.display.set_caption("Nom du jeu")
        self.clock = pygame.time.Clock()
        self.paused = -1
        self.state = "running"
        self.last_spawned = 0
        self.load_data()

    def load_data(self):
        self.bg = pygame.image.load(os.path.join(img_dir, "bg.jpg"))
        self.bg = pygame.transform.scale(self.bg, (DEFAULT_WIDTH, DEFAULT_HEIGHT + 100))
        self.menu_group = pygame.sprite.Group()
        self.player = Player(self, 10, 2)
        for i in range(8):
            Obstacles(self)
        self.map = TiledMap_Manager(self)
        self.map.chunk_spawning()

    def map_update(self):
        self.map.update()
        self.map.screen_scrolling()
        self.map.chunk_killing()
        self.map.chunk_spawning()

    def spawn_asteroids(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawned > OBS_SPAWN_RATE:
            self.last_spawned = now
            Obstacles(self)

    def update(self):
        if self.state != "paused":
            map_group.update()
            self.spawn_asteroids()
            all_sprites.update()
            self.map_update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        if self.state != "paused":
            try:
                for sprite in self.menu_group:
                    sprite.kill()
            except Exception:
                pass
        else:
            self.menu = Pause(DEFAULT_WIDTH/2, DEFAULT_HEIGHT/2)
            self.menu_group.add(self.menu)
            self.menu_group.draw(self.screen)

        map_group.draw(self.screen)
        all_sprites.draw(self.screen)
        pygame.display.flip()

    def pause_menu(self):
        self.paused += 1
        if self.paused % 2 == 0:
            self.state = "paused"
            print(self.state)
        else:
            self.state = "running"

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    pass
                if event.key == pygame.K_o:
                    pass
                if event.key == pygame.K_ESCAPE:
                    self.pause_menu()

    def run(self):
        while True:
            self.dt = self.clock.tick(60) / 100 * FPS
            self.events()
            self.update()
            self.draw()