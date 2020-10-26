import os

# Paths
current_dir = os.path.dirname(__file__)
main_dir = os.path.join(current_dir, "../")
data_dir = os.path.join(current_dir, "../data")
img_dir = os.path.join(current_dir, "../data/img")
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
PLAYER_ACCELERATION = 0.05
PLAYER_FRICTION = -0.03
PLAYER_GRAV = 0.1
PLAYER_JUMP_FORCE = -8

# Level settings
SCROLL_RATE = 0#0.0001
# Colors & Misc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)