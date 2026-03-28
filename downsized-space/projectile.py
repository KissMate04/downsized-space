"""
Module for handling projectiles in the game.

Projectiles are fired by the player and enemies and cause damage on collision.
"""
import pygame


class Projectile:
    """
    Projectile class representing projectiles fired by ships.

    Projectiles move vertically and damage ships on collision.
    Their appearance and direction depend on who fired them.
    """

    def __init__(self, x, y, size, speed, damage, shooter):
        """
        Initialize a Projectile with given parameters.

        Args:
            x: Initial x-coordinate
            y: Initial y-coordinate
            size: Size of the projectile
            speed: Movement speed of the projectile
            damage: Damage the projectile deals on hit
            shooter: Reference to the entity that fired the projectile ("player" or enemy object)
        """
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.damage = damage
        self.hitbox = pygame.Rect(
            self.x,
            self.y - self.size * 1.5,
            min(self.size / 4, 15),
            min(self.size, 40)
        )
        self.shooter = shooter

    def move(self):
        """
        Move the projectile vertically.

        Player projectiles move upward, while enemy projectiles move downward.
        Updates the hitbox position accordingly.
        """
        if self.shooter == "player":
            self.y -= self.speed
        else:
            self.y += self.speed
        self.hitbox = pygame.Rect(
            self.x,
            self.y - self.size * 1.5,
            min(self.size / 4, 15),
            min(self.size, 40)
        )

    def draw(self, screen):
        """
        Draw the projectile on the screen.

        Player projectiles are orange, while enemy projectiles are blue.

        Args:
            screen: The pygame surface to draw on
        """
        if self.shooter == "player":
            pygame.draw.rect(screen, (255, 100, 0), self.hitbox)
        else:
            pygame.draw.rect(screen, (100, 100, 255), self.hitbox)
