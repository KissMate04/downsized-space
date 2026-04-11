"""
Module for handling the player's ship in the game.

The player ship is controlled by keyboard input and can shoot projectiles.
"""
import pygame
from . import ship

class Player(ship.Ship):
    """
    Player ship class that inherits from Ship.

    The player can move in all directions using keyboard controls,
    shoot projectiles, and resize their ship using the mouse wheel.
    """
    def __init__(self, max_health, base_damage, speed, x, y, game_parameters, assets):
        """
        Initialize the Player with given parameters.

        Args:
            max_health: Maximum health of the player. On a new level this is the remaining health from the previous level
            base_damage: Base damage the player deals
            speed: Movement speed of the player
            x: spawn coordinate: x
            y: spawn coordinate: y
            game_parameters: Game parameters
            assets: Game assets
        """
        super().__init__(max_health, base_damage, speed, x, y, game_parameters, assets)
        self.cooldown = 0
        self.max_size = self.game_parameters.game_area.width // 4.5 - ((self.game_parameters.game_area.width // 4.5) % 16)

    def resize(self, eventy):
        """
        Resize the player's ship based on mouse wheel input.

        Increases or decreases the ship size, which affects its damage output.
        Size is limited to a range between 32 and 176.

        Args:
            eventy: Mouse wheel direction (1 for increase, -1 for decrease)
        """
        if eventy == 1 and self.shipsize < self.max_size:
            self.shipsize += 16
        if eventy == -1 and self.shipsize > max(48, self.max_size - (16*10)):
            self.shipsize -= 16
        super().resize()
        super().move() # ensures ship stays in bounds after resizing

    def move(self, keys):
        """
        Move the player based on keyboard input.

        Handles movement in four directions (up, down, left, right)
        using arrow keys or WASD.

        Args:
            keys: Keyboard state to determine which direction to move
        """
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        self.y = max(self.y, self.game_parameters.player_area.top)
        super().move()

    def hit(self, damage_taken):
        """
        Handle the player being hit by an enemy projectile.

        Args:
            damage_taken: Amount of damage to subtract from health
        """
        super().hit(damage_taken)

    def death(self):
        """
        Handle player death.

        Triggers game over when the player dies.
        """
        pygame.event.post(pygame.event.Event(self.game_parameters.player_death))

    def shoot(self):
        """
        Create a projectile fired by the player.

        The projectile is added to the global projectiles list.
        The cooldown is scaled with player size (bigger -> longer cooldown)
        """
        if pygame.time.get_ticks() - self.cooldown > 110 + self.shipsize * 1.65:
            self.cooldown = pygame.time.get_ticks()
            return True
        return False

    def __str__(self):
        return "Player"
