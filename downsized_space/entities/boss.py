"""
Module for handling boss enemy behavior in the game.
Bosses are special enemies with unique movement patterns and behavior.
"""
import random
import pygame
from . import enemy


class Boss(enemy.Enemy):
    """
    Boss enemy class that inherits from Enemy.

    Bosses have different movement patterns
    and more health/damage than regular enemies.
    They can move in any direction and change direction randomly or when hit.
    """

    def __init__(self, max_health, base_damage, speed, x, y, game_parameters, assets):
        """
        Initialize the Boss with given parameters.

        Args:
            max_health: Maximum health of the boss
            base_damage: Base damage the boss deals
            speed: Movement speed of the boss
            x: spawn coordinate: x
            y: spawn coordinate: y
            game_parameters: Game parameters
            assets: Game assets
        """
        super().__init__(max_health, base_damage, speed, x, y, game_parameters, assets)
        # Added to score when killed.
        self.value = 60


    def move(self):
        """
        Move the boss according to its current direction.

        Bosses bounce off the screen edges.

        Args:
            keys: Keyboard state (not used for boss movement)
        """
        if self.dying:
            if pygame.time.get_ticks() - self.time > 500:
                self.alive = False
            return

        self.x += self.speed * self.xdirection
        self.y += self.speed * self.ydirection
        # hit right wall, bounce left
        if self.x >= self.game_parameters.enemy_area.left + self.game_parameters.enemy_area.width - self.image.get_width():
            self.xdirection = -1
        # hit bottom wall, bounce up
        elif self.y >= self.game_parameters.enemy_area.bottom - self.shipsize:
            self.ydirection = -1
        # hit left wall, bounce right
        elif self.x <= self.game_parameters.enemy_area.left:
            self.xdirection = 1
        # hit top wall, bounce down
        elif self.y <= self.game_parameters.enemy_area.top:
            self.ydirection = 1

        # Random chance to direction (1% by default)
        if (random.random() < self.game_parameters.chance_of_direction_change) and not self.dying:
            self.change_direction()

        super().move()

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

    def death(self):
        super().death()

    def __str__(self):
        return "Boss"