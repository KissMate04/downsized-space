"""
Module for managing game state and global game settings.

Contains global variables for game settings, state tracking,
and lists of game objects (projectiles, enemies).
"""

import pygame

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
BOSS_BASE_DAMAGE = 60
CHANCE_OF_DIRECTION_CHANGE = 0.01   # 0.01 = 1% chance
# projectile
PROJECTILE_SPEED = 6
# score to progress
LEVEL1_TARGET_SCORE = 100
LEVEL2_TARGET_SCORE = 500
LEVEL3_TARGET_SCORE = 800
# End of settings

font = pygame.font.SysFont('Futura', 20)
game_over_font = pygame.font.SysFont('Rocket', 100)
menu_font = pygame.font.SysFont('Futura', 90)
level_font = pygame.font.SysFont('Helvetica', 60)

"""
Initializes the game, creates player and starts the game loop.
"""
#fonts

score = 0
running = True
in_menu = True

