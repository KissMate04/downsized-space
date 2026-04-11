"""
Module for global game settings.
"""
import pygame

class Settings:
    """A class for the settings of the game.

    None of these variables should be changed.

    Args:
    player_max_health: The maximum health of the player.
    player_base_damage: The base damage of the player. It scales with player size. With 53 smallest size kills in 6 shots, biggest kills in 2 shots.
    enemy_max_health: The maximum health of the enemies.
    enemy_base_damage: The base damage of the enemies. It scales with enemy size.
    enemy_speed: The speed of the enemies.
    enemy_shot_timer: The time between enemy shots in milliseconds.
    boss_max_health: The maximum health of the boss.
    boss_base_damage: The base damage of the boss. It scales with boss size.
    boss_speed: The speed of the boss.
    projectile_speed: The speed of the projectiles.
    """
    #def __init__(self,screen, player_max_health = 100, player_base_damage = 53 , enemy_max_health = 100, enemy_base_damage = 30, enemy_speed = 3.5, enemy_shot_timer = 800, boss_max_health = 200, boss_base_damage = 50, boss_speed = 5, projectile_speed = 6):
    def __init__(self, screen, **kwargs):
        self.fps = 60
        #Entities
        #player
        self.player_max_health = kwargs.get("player_max_health",100)
        self.player_base_damage = kwargs.get("player_base_damage" ,53)
        self.player_speed = 4
        self.player_death = pygame.USEREVENT + 2
        #enemy
        self.enemy_max_health = kwargs.get("enemy_max_health", 100)
        self.enemy_base_damage = kwargs.get("enemy_base_damage", 30)
        self.enemy_speed = kwargs.get("enemy_speed", 3.5)
        self.enemy_shot = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_shot, kwargs.get("enemy_shot_timer", 800))
        # boss
        self.boss_max_health = kwargs.get("boss_max_health", 200)
        self.boss_base_damage = kwargs.get("boss_base_damage", 50)
        self.boss_speed = kwargs.get("boss_speed",5)
        self.chance_of_direction_change = 0.01 # 0.01 = 1% chance of changing direction each frame
        # projectile
        self.projectile_speed = kwargs.get("projectile_speed", 6)
        #screen dimensions
        self.screen = screen  # the entire scrren
        self.screen_width, self.screen_height = self.screen.get_size()
        self.game_width = int(self.screen_width * 0.4)  # width of the game area
        self.side_width = (self.screen_width - self.game_width) // 2  # width of each side panel
        self.game_area = pygame.Rect(
            self.side_width*1.01,
            self.screen_height * 0.02,
            self.game_width * 0.99,
            self.screen_height * 0.99
        ) # the area where the game takes place, with padding for better visuals.
        # enemy spawn points
        self.enemy_area = pygame.Rect(self.game_area.left, self.game_area.top, self.game_area.width,
                                      self.game_area.height * 0.39) # Enemies can only move in the top 39% of the game area.
        self.player_area = pygame.Rect(self.game_area.left, self.game_area.height * 0.4, self.game_area.width, self.game_area.height * 0.6) # Player can only move in the bottom 60% of the game area.
        """
        Spawn coordinates for enemies. Each level loads 2 more than the previous.
        """
        self.spawn_points = [
            (0, 0), (1, 0),
            (0, 1), (1, 1),
            (0.33, 0), (0.66, 0),
            (0.33, 1), (0.66, 1),
            (0, 0.5), (1, 0.5)
        ]