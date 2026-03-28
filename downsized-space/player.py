# pylint: disable=import-error, no-member
"""
Module for handling the player's ship in the game.

The player ship is controlled by keyboard input and can shoot projectiles.
"""
import pygame
import ship
import game



class Player(ship.Ship):
    """
    Player ship class that inherits from Ship.

    The player can move in all directions using keyboard controls,
    shoot projectiles, and resize their ship using the mouse wheel.
    """
    def __init__(self, image, max_health, base_damage, speed, x, y):
        """
        Initialize the Player with given parameters.

        Args:
            screen: The pygame surface to draw on
            image: The filename of the player's sprite image
            max_health: Maximum health of the player
            base_damage: Base damage the player deals
            speed: Movement speed of the player
            x: spawn coordinate: x
            y: spawn coordinate: y
        """
        super().__init__(image, max_health, base_damage, speed, x, y)
        self.cooldown = 0

    def resize(self, eventy):
        """
        Resize the player's ship based on mouse wheel input.

        Increases or decreases the ship size, which affects its damage output.
        Size is limited to a range between 32 and 176.

        Args:
            eventy: Mouse wheel direction (1 for increase, -1 for decrease)
        """
        if eventy == 1 and self.shipsize < 176:
            self.shipsize += 16
        if eventy == -1 and self.shipsize > 48:
            self.shipsize -= 16
        self.damage = self.base_damage * (self.shipsize / 100)
        self.image = pygame.transform.scale(
            self.image, (self.shipsize, self.shipsize))
        self.hitbox = pygame.Rect(
            self.x,
            self.y,
            self.image.get_width(),
            self.image.get_height())


    def move(self, area, keys):
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
        self.y = max(self.y, area.top+300+self.shipsize)
        super().move(area)

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
        print("you have died.")
        pygame.event.post(pygame.event.Event(game.PLAYER_DEATH))

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
