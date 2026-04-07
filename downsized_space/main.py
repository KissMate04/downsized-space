"""
Contains the game loop.
"""
import sys
import pygame
from .scenes.main_menu import MainScreen
from .scenes.level import LevelScene
from .scenes.settings_scene import SettingsScreen
from .scenes.game_over import GameOverScreen
from. import settings

def main():
    current_scene = "main_menu"
    pygame.font.init()
    pygame.mixer.init()

    LEVEL = [
        (0, 0), (1, 0),
        (0, 1),(1, 1),
        (0.33, 0),(0.66, 0),
        (0.33, 1),(0.66, 1),
        (0, 0.5),(1, 0.5)
    ]
    """
    Spawn coordinates for enemies. Each level loads 2 more than the previous.
    """

    clock = pygame.time.Clock()

    def make_scene(name,num=0):
        if name == "main_menu":
            pygame.time.wait(250) # to avoid clicking from the previous scene effecting the menu
            pygame.mixer.music.load(settings.get_resource_path("downsized_space/audio/music_menu.wav"))
            pygame.mixer.music.play(-1)
            return MainScreen()
        if name == "settings":
            pygame.time.wait(250)  # to avoid clicking from the previous scene effecting the menu
            return SettingsScreen()
        if name == "level":
            if num < 2: # This allows continuous music playing between levels
                pygame.mixer.music.load(settings.get_resource_path("downsized_space/audio/music_game.wav"))
                pygame.mixer.music.play(-1)
            return LevelScene(LEVEL[0:min(len(LEVEL),num*2)], num)
        if name == "over":
            pygame.mixer.music.unload()
            return GameOverScreen()
        return MainScreen()

    current_scene_name = "main_menu"
    level_num = 0
    current_scene = make_scene(current_scene_name)

    while True:
        events = pygame.event.get()
        if any(event.type == pygame.QUIT for event in events):
            pygame.quit()
            sys.exit()

        next_scene = current_scene.handle_events(events)

        if next_scene[0] == "QUIT":
            pygame.quit()
            sys.exit()

        if next_scene[0] != current_scene_name or next_scene[1] != level_num:
            current_scene_name = next_scene[0]
            level_num += 1
            if current_scene_name == "main_menu":
                level_num = 0
                pass
            current_scene = make_scene(current_scene_name, level_num)

        current_scene.update(events)
        current_scene.draw()

        pygame.display.flip()
        clock.tick(settings.FPS)

if __name__ == "__main__":
    main()
