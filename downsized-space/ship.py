# pylint : disable=import-error, no-member
"""
Module containing the base Ship class for the game.

All player and enemy ships inherit from this base class.
"""
import os
import pygame


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
            screen: The pygame surface to draw on
            image: The filename of the ship's sprite image
            max_health: Maximum health of the ship
            base_damage: Base damage the ship deals
            speed: Movement speed of the ship
            x: spawn coordinate: x
            y: spawn coordinate: y
        """
        self.shipsize = 48
        self.image = pygame.image.load(
            os.path.join('sprites', image)).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.shipsize, self.shipsize))
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

    def move(self, area):  # pylint: disable=unused-argument
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
        self.x = max(self.x, area.left)
        self.y = max(self.y, area.top)
        self.x = min(self.x, area.left + area.width - self.shipsize)
        self.y = min(self.y, area.height - self.shipsize)

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

    def death(self):
        """
        Handles ship's death
        """
        pass
