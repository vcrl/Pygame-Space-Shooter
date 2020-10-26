import pygame, sys, os, random
from .sprites import all_sprites, map_group, Player
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
        self.load_data()

    def load_data(self):
        self.menu_group = pygame.sprite.Group()
        self.player = Player(self, 10*TILESIZE, 10)
        self.map = TiledMap_Manager(self)
        self.map.chunk_spawning()

    def update(self):
        if self.state != "paused":
            map_group.update()
            all_sprites.update()
            self.map.update()
            self.map.screen_scrolling()
            self.map.chunk_killing()
            self.map.chunk_spawning()

    def draw(self):
        self.screen.fill(BLACK)
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
                    self.player.state["debug_mode"] = True

                if event.key == pygame.K_SPACE:
                    for sprite in map_group:
                        sprite.kill()
                if event.key == pygame.K_ESCAPE:
                    self.pause_menu()


    def run(self):
        while True:
            self.dt = self.clock.tick(FPS) / 100 * FPS
            self.events()
            self.update()
            self.draw()