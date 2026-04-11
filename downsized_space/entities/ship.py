"""
Module containing the base Ship class for the game.

All player and enemy ships inherit from this base class.
"""
import pygame
from abc import ABC, abstractmethod

class Ship(ABC):
    """
    Base class for all ships in the game.

    Provides common functionality for player and enemy ships,
    including movement, health management, and collision detection.
    """

    def __init__(self, max_health, base_damage, speed, x, y, game_parameters, assets):
        """
        Initialize a Ship with given parameters.

        Args:
            image: The filename of the ship's sprite image
            max_health: Maximum health of the ship
            base_damage: Base damage the ship deals
            speed: Movement speed of the ship
            x: spawn coordinate: x
            y: spawn coordinate: y
        """
        self.game_parameters = game_parameters
        self.assets = assets

        self.max_size = self.assets.max_size
        self.shipsize = self.assets.shipsize

        self.image = assets.sprites[str(self)]

        self.max_health = max_health
        self.health = max_health
        self.base_damage = base_damage
        self.damage = base_damage * (self.shipsize / 100)
        self.speed = speed
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(
            self.x,
            self.y,
            self.image.get_width(),
            self.image.get_height())

    @abstractmethod
    def move(self):
        """
        Base movement method for ships.

        Updates the hitbox position and keeps the ship within screen bounds.

        Args:
            keys: Keyboard state (used by subclasses)
        """
        self.x = max(self.x, self.game_parameters.game_area.left)
        self.y = max(self.y, self.game_parameters.game_area.top)
        self.x = min(self.x, self.game_parameters.game_area.left + self.game_parameters.game_area.width - self.shipsize)
        self.y = min(self.y, self.game_parameters.game_area.height - self.shipsize)
        self.hitbox.topleft = (self.x, self.y)

    def hit(self, damage_taken):
        """
        Handle the ship being hit by a projectile.

        Reduces health by the damage amount and triggers death if health <= 0.

        Args:
            damage_taken: Amount of damage to subtract from health
        """
        self.health -= round(damage_taken)
        if self.health <= 0:
            return self.death()
        return None

    def resize(self):
        """
        Base resize method for ships.

        Player resizes with mouse scroll, enemy after successful hits.
        """
        self.damage = self.base_damage * (self.shipsize / 100)
        self.image = self.assets.scale_sprite(self.image, self.shipsize, self.shipsize)
        self.hitbox = pygame.Rect(
            self.x,
            self.y,
            self.image.get_width(),
            self.image.get_height())

    @abstractmethod
    def death(self):
        """
        Handles ship's death
        """
        pass

    def __str__(self):
        return "Ship"