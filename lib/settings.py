import os

# Paths
current_dir = os.path.dirname(__file__)
main_dir = os.path.join(current_dir, "../")
data_dir = os.path.join(current_dir, "../data")
img_dir = os.path.join(current_dir, "../data/img")
fruits_dir = os.path.join(current_dir, "../data/img/fruits")
maps_dir = os.path.join(current_dir, "../data/maps")

# Games
TILESIZE = 32
FPS = 60

# Settings
DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

CHUNK_WIDTH = 40 * 32
CHUNK_HEIGHT = 23 * 32

FULL_SCREEN_WIDTH = 1200
FULL_SCREEN_HEIGHT = 1200

# Player settings
PLAYER_IMG = os.path.join(img_dir, "player.png")
PLAYER_ACCELERATION = 0.25
PLAYER_SPRINT_ACCELERATION = 0.35
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.3
PLAYER_JUMP_FORCE = 5
BULLET_RATE  = 150
HIT_RATE = 1000

# Level settings
OBS_SPAWN_RATE = 3000
SCROLL_RATE = 0#0.00015
OBS_GRAV = 6
# Colors & Misc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)