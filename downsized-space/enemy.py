# pylint: disable=import-error, no-member, attribute-defined-outside-init
"""
Module for handling enemy ships in the game.
"""
import os
import pygame
import ship
import game
import projectile


class Enemy(ship.Ship):
    """
    Enemy ship class that inherits from Ship.

    Enemies follow a rectangular movement pattern, shoot at the player,
    and are upgraded (promoted) when they hit the player.
    """
    def __init__(self, image, max_health, base_damage, speed, x, y):
        """
        Initialize an Enemy with given parameters.

        Args:
            screen: The pygame surface to draw on
            image: The filename of the enemy's sprite image
            max_health: Maximum health of the enemy
            base_damage: Base damage the enemy deals
            speed: Movement speed of the enemy
            x: spawn coordinate: x
            y: spawn coordinate: y
        """
        super().__init__(image, max_health, base_damage, speed, x, y)
        self.alive = True
        self.xdirection = 1
        self.ydirection = 0
        self.dying = False
        self.time = 0

    def move(self, area):
        """
        Move the enemy ship according to a rectangular pattern.

        Args:
            keys: Keyboard state (not used for enemy movement)
        """
        if self.dying:
            if pygame.time.get_ticks() - self.time > 500:
                self.alive = False
            return

        self.x += self.speed * self.xdirection
        self.y += self.speed * self.ydirection
        if (self.x >= area.left + area.width - self.image.get_width() - 50 and self.ydirection == 0):
            self.xdirection = 0
            self.ydirection = 1
        elif self.y >= 300 and self.xdirection in (0, 1):
            self.xdirection = -1
            self.ydirection = 0
        elif self.x <= area.left + 50 and self.ydirection == 0:
            self.xdirection = 0
            self.ydirection = -1
        elif self.y <= area.top + 30 and self.xdirection == 0:
            self.xdirection = 1
            self.ydirection = 0

        super().move( area)

    def death(self):
        """
        Handle enemy death.

        Changes the enemy sprite to an explosion, increases the score,
        and marks the enemy for removal after a delay.
        """
        if not self.dying:
            self.image = pygame.image.load(
                os.path.join('sprites', 'explosion.png')).convert_alpha()
            self.image = pygame.transform.scale(
                self.image, (self.shipsize, self.shipsize))
            game.score += 20
            self.dying = True
            self.time = pygame.time.get_ticks()
            print("score: ", game.score)

    def promotion(self):
        """
        Upgrade the enemy when it successfully hits the player.

        Increases the enemy's size and damage.
        """
        self.shipsize += 16
        self.damage = self.base_damage * (self.shipsize / 100)
        self.image = pygame.transform.scale(
            self.image, (self.shipsize, self.shipsize))
        self.hitbox = pygame.Rect(
            self.x,
            self.y,
            self.image.get_width(),
            self.image.get_height())

    def shoot(self):
        """
        Create a projectile fired by the enemy.

        The projectile is added to the global projectiles list.
        Does nothing if the enemy is in the dying state.
        """
        if self.dying:
            return False
        return True

