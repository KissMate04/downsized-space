"""
Module containing the base Ship class for the game.

All player and enemy ships inherit from this base class.
"""
import os
import pygame
from .. import settings

class Ship:
    """
    Base class for all ships in the game.

    Provides common functionality for player and enemy ships,
    including movement, health management, and collision detection.
    """

    def __init__(self, image, max_health, base_damage, speed, x, y):
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
        self.area = settings.GAME_AREA
        max_size = self.area.width // 4.5 - ((self.area.width // 4.5) % 16) # size depends on the screen size
        self.shipsize = max(48, max_size - (16*8))

        self.image = pygame.image.load(
            os.path.join('downsized-space', 'sprites', image)).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.shipsize, self.shipsize))

        self.max_health = max_health
        self.health = max_health
        self.base_damage = base_damage
        self.damage = base_damage * (self.shipsize / 120)
        self.speed = speed
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(
            self.x,
            self.y,
            self.image.get_width(),
            self.image.get_height())

    def move(self):
        """
        Base movement method for ships.

        Updates the hitbox position and keeps the ship within screen bounds.

        Args:
            keys: Keyboard state (used by subclasses)
        """
        self.hitbox = pygame.Rect(
            self.x,
            self.y,
            self.image.get_width(),
            self.image.get_height())
        self.x = max(self.x, self.area.left*1.01)
        self.y = max(self.y, self.area.top)
        self.x = min(self.x, self.area.left + self.area.width*0.99 - self.shipsize)
        self.y = min(self.y, self.area.height*0.99 - self.shipsize)

    def hit(self, damage_taken):
        """
        Handle the ship being hit by a projectile.

        Reduces health by the damage amount and triggers death if health <= 0.

        Args:
            damage_taken: Amount of damage to subtract from health
        """
        self.health -= round(damage_taken)
        if self.health <= 0:
            self.death()

    def resize(self):
        """
        Base resize method for ships.

        Player resizes with mouse scroll, enemy after successful hits.
        """
        self.damage = self.base_damage * (self.shipsize / 100)
        self.image = pygame.transform.scale(
            self.image, (self.shipsize, self.shipsize))
        self.hitbox = pygame.Rect(
            self.x,
            self.y,
            self.image.get_width(),
            self.image.get_height())

    def death(self):
        """
        Handles ship's death
        """
        pass
