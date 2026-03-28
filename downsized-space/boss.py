# pylint: disable=import-error, no-member, attribute-defined-outside-init
"""
Module for handling boss enemy behavior in the game.
Bosses are special enemies with unique movement patterns and behavior.
"""
import random
import pygame
import enemy
import game
import ship


class Boss(enemy.Enemy):
    """
    Boss enemy class that inherits from Enemy.

    Bosses have different movement patterns
    and more health/damage than regular enemies.
    They can move in any direction and change direction randomly or when hit.
    """

    def __init__(self, image, max_health, base_damage, speed, x, y):
        """
        Initialize the Boss with given parameters.

        Args:
            screen: The pygame surface to draw on
            image: The filename of the boss's sprite image
            max_health: Maximum health of the boss
            base_damage: Base damage the boss deals
            speed: Movement speed of the boss
            x: spawn coordinate: x
            y: spawn coordinate: y
        """
        super().__init__(image, max_health, base_damage, speed, x, y)

    def move(self):
        """
        Move the boss according to its current direction.

        Bosses bounce off the screen edges.

        Args:
            keys: Keyboard state (not used for boss movement)
        """
        if self.dying:
            if pygame.time.get_ticks() - self.time > 500:
                game.enemies.remove(self)
            return

        self.x += self.speed * self.xdirection
        self.y += self.speed * self.ydirection
        if self.x >= self.screen.get_width() - self.image.get_width() - 20:
            self.xdirection = -1
        elif self.x <= 20:
            self.xdirection = 1
        if self.y >= 350:
            self.ydirection = -1
        elif self.y <= 30:
            self.ydirection = 1

        # Random chance to direction (1% by default)
        if (random.random() < game.CHANCE_OF_DIRECTION_CHANGE
                and not self.dying):
            self.change_direction()

        ship.Ship.move(self)

    def change_direction(self):
        """
        Change the boss's movement direction randomly.

        Selects a random direction from 8 possible directions.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]
        random_direction = random.choice(directions)
        self.xdirection = random_direction[0]
        self.ydirection = random_direction[1]

    def hit(self, damage_taken):
        """
        Handle the boss being hit by a projectile.

        When hit, the boss will change direction randomly and take damage.

        Args:
            damage_taken: Amount of damage to subtract from health
        """
        super().hit(damage_taken)

        # Randomly change direction when hit
        if not self.dying:
            self.change_direction()
