import os
import sys
import pygame

class AssetManager:
    """
    A class to manage game assets such as sprites, music, and sounds.
    """
    def __init__(self, side_width, screen_height, game_width):
        """
        Loads all sound effects, the game background and fonts
        :param side_width:
        :param screen_height:
        :param game_width:
        """
        pygame.font.init()
        pygame.mixer.init()

        # sounds
        self.sounds = {
            "player_shot": pygame.mixer.Sound(self.get_resource_path("downsized_space/audio/player_shot.wav")),
            "enemy_explosion": pygame.mixer.Sound(self.get_resource_path("downsized_space/audio/enemy_explosion.wav"))
        }

        self.max_size = game_width // 5 - ((game_width // 5) % 16)  # size depends on the screen size
        self.shipsize = max(48, self.max_size - (16 * 10))

        #sprites
        self.sprites = {
            "Player": self.load_sprite("startership.png", self.shipsize, self.shipsize),
            "Enemy": self.load_sprite("enemyship1.png", self.shipsize, self.shipsize),
            "Boss": self.load_sprite("enemyship2.png", self.shipsize, self.shipsize),
            "explosion": self.load_sprite("explosion.png", self.shipsize, self.shipsize)
        }

        # backgrounds
        self.left_panel = self.load_sprite("leftpanel.png", side_width, screen_height)
        self.right_panel = self.load_sprite("rightpanel.png", side_width, screen_height)
        self.area_panel = self.load_sprite("areapanel.png", game_width, screen_height)

        # fonts
        self.font = pygame.font.SysFont('Futura', 20)
        self.game_over_font = pygame.font.SysFont('Rocket', 100)
        self.menu_font = pygame.font.SysFont('Futura', 90)
        self.level_font = pygame.font.SysFont('Helvetica', 60)

    def load_sprite(self, filename, size_width, size_height):
        """
            Loads a sprite from the given filename and scales it to the given size.
            Assumes the audio file is in the "sprites" folder and is a .png file.
        :param filename: The name of the sprite file (including extension).
        :param size_width: New width of the sprite.
        :param size_height: New height of the sprite.
        :return: The loaded and scaled sprite.
        """
        sprite = pygame.image.load(
            self.get_resource_path(
                os.path.join('downsized_space','sprites', filename))).convert_alpha()
        return self.scale_sprite(sprite, size_width, size_height)

    def scale_sprite(self, sprite, size_width, size_height):
        """
        Scales the given sprite to the given size.
        :param sprite: The sprite to be scaled.
        :param size_width: New width of the sprite.
        :param size_height: New height of the sprite.
        :return: The resized sprite.
        """
        return pygame.transform.scale(sprite, (size_width, size_height))

    def load_music(self, filename):
        """Loads the music from the given filename.
        Assumes the audio file is in the "audio" folder.
        :param filename: The name of the music file (including extension).
        """
        pygame.mixer.music.load(
            self.get_resource_path(
                os.path.join('downsized_space','audio', filename)))

    def unload_music(self):
        """
            Unloads the currently loaded music.
        """
        pygame.mixer.music.unload()

    def get_resource_path(self, relative_path):
        """Return an absolute path that works for source runs and PyInstaller builds."""
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
        return os.path.join(base_path, relative_path)