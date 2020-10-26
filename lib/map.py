import os, pytmx, pygame, random
from .sprites import Player, Wall, Obstacles,all_sprites, walls, map_group, obstacles
from .settings import *
vec = pygame.math.Vector2

class MapFromFile:
    def __init__(self, game):
        self.game = game
        self.map = dict()
        self.map_data = list()
        self.scroll = [2, 0]
        self.walls = list()

    def screen_scrolling(self):
        """
        Screen scrolling management
        """
        self.scroll[0] += 0.0001 * self.game.dt
        for sprite in walls:
            sprite.pos.x -= int(self.scroll[0])
            sprite.pos.y -= int(self.scroll[1])
        #self.scroll[0] += (self.player.pos.x - self.scroll[0] - DEFAULT_WIDTH/2)
        #self.scroll[1] += (self.player.pos.y - self.scroll[1] - DEFAULT_HEIGHT/2)

    def load_nonfile_map(self):
        """
        Load map components outside a map.txt file
        """
        self.walls.append(Wall(self.game, 0, DEFAULT_HEIGHT-100, DEFAULT_WIDTH, 100))
        self.player = Player(self.game, 1, 1)

    def load_infinite_tiles(self):
        """
        Map management for loading infinite tiles
        """
        self.walls.append(Wall(self.game, 0, DEFAULT_HEIGHT-100, DEFAULT_WIDTH, 100))
        self.player = Player(self.game, 2, 2)

    def kill_walls(self):
        """
        Method to kill walls outside the screen for performance reasons
        """
        for wall in walls:
            if wall.rect.topright[0] < 1:
                print("oui")
                wall.kill()
                self.walls.remove(wall)

    def spawn_walls(self):
        """
        Method to spawn walls
        """
        for wall in walls:
            print(len(self.walls))
            if len(self.walls) < 2:
                if wall.rect.x < 1:
                    self.walls.append(Wall(self.game, wall.rect.width, DEFAULT_HEIGHT-100, DEFAULT_WIDTH, 100))

    def load_data(self):
        """
        Data loading for a map from a file
        """
        with open(os.path.join(maps_dir, "map.txt"), "r") as f:
            for line in f:
                self.map_data.append(line)
                self.load_level()
    
    def load_level(self):
        """
        Leveling loading for a map from a file
        """
        for col, tiles in enumerate(self.map_data):
                    for row, tile in enumerate(tiles):
                        if tile == "1":
                            self.walls.append(Wall(self.game, row, col, TILESIZE, TILESIZE))

class TiledMap(pygame.sprite.Sprite):
    def __init__(self, game, filename, x, y):
        self.game = game
        self.groups = map_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.image = self.make_map()
        self.rect = self.image.get_rect()
        self.walls = list()
        self.pos = vec(x, y)
        self.scroll = [0, 0]
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.state = {
            "moving" : False
        }
        self.load_data()

    def screen_scrolling(self):
        """
        Screen scrolling management
        """
        self.state["moving"] = True
        self.scroll[0] += 0.0001 * self.game.dt
        self.rect.x -= int(self.scroll[0])
        for wall in walls:
            wall.rect.x -= int(self.scroll[0])
            wall.rect.y -= int(self.scroll[1])
        #for sprite in all_sprites:
        #    sprite.rect.x -= int(self.scroll[0])
        #    sprite.rect.y -= int(self.scroll[1])

    def kill_map(self):
        if self.rect.x <= -DEFAULT_WIDTH:
            for wall in walls:
                wall.kill()
            self.kill()

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
    
    def load_data(self):
        for tile_object in self.tmxdata.objects:
            if tile_object.name == "wall":
                self.walls.append(Wall(self.game, tile_object.x, tile_object.y, tile_object.width, tile_object.height))

    def update(self):
        pass

class TiledMap_Manager:
    def __init__(self, game):
        self.game = game
        self.map = list()
        self.obstacles = list()
        self.map_management = {
            "blocks_spawned" : 1
        }
        self.scroll = [0, 0]
        self.state = {
            "moving" : False,
        }
        self.default_map()
        self.chunk_count = 2

    def update(self):
        self.chunk_count = len(self.map)
    
    def default_map(self):
        self.map.append(TiledMap(self.game, os.path.join(maps_dir, "default.tmx"), 0, 0))
        self.map.append(TiledMap(self.game, os.path.join(maps_dir, "default.tmx"), CHUNK_WIDTH, 0))

    def chunk_killing(self):
        for chunk in self.map:
            if chunk.rect.topright[0] < 1:#-CHUNK_WIDTH:
                self.kill_chunk(chunk)

    def chunk_spawning(self):
        if self.chunk_count < 2:
            self.map.append(TiledMap(self.game, os.path.join(maps_dir, "default.tmx"), CHUNK_WIDTH-TILESIZE, 0))
            self.obstacles.append(Obstacles(
                self,
                self.game, 
                random.randint(0, DEFAULT_WIDTH/TILESIZE), #x
                -1, #y
                random.randint(TILESIZE, TILESIZE*5), #w
                random.randint(TILESIZE, TILESIZE*5) #h
                ))
            self.obstacles.append(Obstacles(
                self,
                self.game, 
                random.randint((DEFAULT_WIDTH/TILESIZE)/2, DEFAULT_WIDTH/TILESIZE), #x
                -1, #y
                random.randint(TILESIZE, TILESIZE*5), #w
                random.randint(TILESIZE, TILESIZE*5) #h
                ))
            self.obstacles.append(Obstacles(
                self,
                self.game, 
                random.randint(0, DEFAULT_WIDTH/TILESIZE), #x
                -1, #y
                random.randint(TILESIZE, TILESIZE*5), #w
                random.randint(TILESIZE, TILESIZE*5) #h
                ))
            self.obstacles.append(Obstacles(
                self,
                self.game, 
                random.randint((DEFAULT_WIDTH/TILESIZE)/2, DEFAULT_WIDTH/TILESIZE), #x
                -1, #y
                random.randint(TILESIZE, TILESIZE*5), #w
                random.randint(TILESIZE, TILESIZE*5) #h
                ))
    
    def kill_chunk(self, chunk):
        self.map.remove(chunk)
        for wall in chunk.walls:
            wall.kill()
        for obstacle in obstacles:
            if obstacle.rect.y > DEFAULT_WIDTH:
                obstacle.kill()
        chunk.kill()


    def screen_scrolling(self):
        self.state["moving"] = True
        for obs in obstacles:
            print(obs.rect.x)
            obs.pos.x -= int(self.scroll[0])
            obs.pos.y -= int(self.scroll[1])
        for maps in self.map:
            maps.state["moving"] = True
            self.scroll[0] += SCROLL_RATE * self.game.dt
            maps.rect.x -= int(self.scroll[0])
            for wall in maps.walls:
                wall.rect.x -= int(self.scroll[0])
                wall.rect.y -= int(self.scroll[1])