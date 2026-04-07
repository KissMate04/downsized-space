"""
Module for managing game state and global game settings.

Contains global variables for game settings, state tracking,
and lists of game objects (projectiles, enemies).
"""

import os
import sys

import pygame


def get_resource_path(relative_path):
    """Return an absolute path that works for source runs and PyInstaller builds."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


pygame.init()

# Settings:
# general
FPS = 60
# enemy shooting cooldown
ENEMY_SHOOT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_SHOOT, 800)
# player
PLAYER_MAX_HEALTH = 100
PLAYER_SPEED = 4
PLAYER_BASE_DAMAGE = 53 # with 53 smallest size kills in 6 shots, biggest kills in 2 shots
PLAYER_DEATH = pygame.USEREVENT + 2
# enemy
ENEMY_MAX_HEALTH = 100
ENEMY_SPEED = 3.5
ENEMY_BASE_DAMAGE = 30
# boss
BOSS_MAX_HEALTH = 200
BOSS_SPEED = 5
BOSS_BASE_DAMAGE = 50
CHANCE_OF_DIRECTION_CHANGE = 0.01   # 0.01 = 1% chance
# volume
MUSIC_VOLUME = 0.5
SOUNDS_VOLUME = 0.5
# projectile
PROJECTILE_SPEED = 6
# End of settings
#fonts
font = pygame.font.SysFont('Futura', 20)
game_over_font = pygame.font.SysFont('Rocket', 100)
menu_font = pygame.font.SysFont('Futura', 90)
level_font = pygame.font.SysFont('Helvetica', 60)


score = 0
running = True
in_menu = True

# Screen dimensions
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # the entire scrren
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
GAME_WIDTH = int(SCREEN_WIDTH * 0.4)  # width of the game area
SIDE_WIDTH = (SCREEN_WIDTH - GAME_WIDTH) // 2  # width of each side area
GAME_AREA = pygame.Rect(
    SIDE_WIDTH,
    10,
    GAME_WIDTH,
    SCREEN_HEIGHT - 10
)

sounds = {
    "player_shot": pygame.mixer.Sound(get_resource_path("downsized_space/audio/player_shot.wav")),
    "enemy_explosion": pygame.mixer.Sound(get_resource_path("downsized_space/audio/enemy_explosion.wav"))
}

#Player
current_health = PLAYER_MAX_HEALTH

# Image paths.
LEFT_PANEL_PATH = get_resource_path(os.path.join('downsized_space','sprites', "leftpanel.png"))
RIGHT_PANEL_PATH = get_resource_path(os.path.join('downsized_space','sprites', "rightpanel.png"))
AREA_PANEL_PATH = get_resource_path(os.path.join('downsized_space','sprites', "areapanel.png"))

class ShipPanels:
    """
    Class that loads the backgournd images
    """
    def __init__(self):
        self.left_panel = pygame.image.load(LEFT_PANEL_PATH).convert_alpha()
        self.left_panel = pygame.transform.scale(
        self.left_panel, (SIDE_WIDTH, SCREEN_HEIGHT))
        self.right_panel = pygame.image.load(RIGHT_PANEL_PATH).convert_alpha()
        self.right_panel = pygame.transform.scale(
            self.right_panel, (SIDE_WIDTH, SCREEN_HEIGHT))
        self.area_panel = pygame.image.load(AREA_PANEL_PATH).convert_alpha()
        self.area_panel = pygame.transform.scale(
            self.area_panel, (GAME_WIDTH, SCREEN_HEIGHT))
