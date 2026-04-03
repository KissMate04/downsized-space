"""
Contains the game loop, levels and the menu.
"""
import sys
import os
import pygame
from .scenes import main_menu, level,game_over
from. import settings

class ShipPanels:
    def __init__(self, gw,sw,sh):
        self.left_panel = pygame.image.load(
            os.path.join('downsized-space','sprites', "leftpanel.png")).convert_alpha()
        self.left_panel = pygame.transform.scale(
        self.left_panel, (sw, sh))
        self.right_panel = pygame.image.load(
            os.path.join('downsized-space','sprites', "rightpanel.png")).convert_alpha()
        self.right_panel = pygame.transform.scale(
            self.right_panel, (sw, sh))
        self.area_panel = pygame.image.load(
            os.path.join('downsized-space','sprites', "areapanel.png")).convert_alpha()
        self.area_panel = pygame.transform.scale(
            self.area_panel, (gw, sh))

def main():
    current_scene = "main_menu"
    pygame.font.init()
    pygame.mixer.init()

    LEVEL1 = [
        (0.1, 0.1),
        (0.8, 0.25)
    ]
    LEVEL2 = [
        (0.1, 0.1),
        (0.8, 0.1),
        (0.1, 0.25),
        (0.8, 0.25)
    ]
    LEVEL3 = [
        (0.25, 0.1),
        (0.5, 0.25),
        (0.75, 0.1),
        (0.25, 0.25),
        (0.75, 0.25)
    ]

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # the entire scrren
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    GAME_WIDTH = SCREEN_WIDTH // 3  # width of the game area
    SIDE_WIDTH = (SCREEN_WIDTH - GAME_WIDTH) // 2  # width of each side area
    GAME_AREA = pygame.Rect(
        SIDE_WIDTH,
        20,
        GAME_WIDTH,
        SCREEN_HEIGHT - 40
    )

    def make_scene(name):
        if name == "main_menu":
            pygame.time.wait(250)
            pygame.mixer.music.load("downsized-space/audio/music_menu.wav")
            pygame.mixer.music.play(-1)
            return main_menu.MainScreen(GAME_AREA)
        if name == "level1":
            pygame.mixer.music.load("downsized-space/audio/music_game.wav")
            pygame.mixer.music.play(-1)
            return level.LevelScene(GAME_AREA, LEVEL1, 1, ShipPanels(GAME_WIDTH, SIDE_WIDTH, SCREEN_HEIGHT))
        if name == "level2":
            pygame.mixer.music.load("downsized-space/audio/music_game.wav")
            pygame.mixer.music.play(-1)
            return level.LevelScene(GAME_AREA, LEVEL2, 2, ShipPanels(GAME_WIDTH, SIDE_WIDTH, SCREEN_HEIGHT))
        if name == "level3":
            pygame.mixer.music.load("downsized-space/audio/music_game.wav")
            pygame.mixer.music.play(-1)
            return level.LevelScene(GAME_AREA, LEVEL3, 3, ShipPanels(GAME_WIDTH, SIDE_WIDTH, SCREEN_HEIGHT))
        if name == "over":
            pygame.mixer.music.unload()
            return game_over.GameOverScreen(GAME_AREA)
        return main_menu.MainScreen(GAME_AREA)

    #TODO írd felul a to stringet
    current_scene_name = "main_menu"
    current_scene = make_scene(current_scene_name)

    while True:
        events = pygame.event.get()
        if any(event.type == pygame.QUIT for event in events):
            pygame.quit()
            sys.exit()

        next_scene = current_scene.handle_events(events)

        if next_scene == "QUIT":
            pygame.quit()
            sys.exit()

        if next_scene != current_scene_name:
            current_scene_name = next_scene
            current_scene = make_scene(current_scene_name)

        current_scene.update(events)
        current_scene.draw(screen)



        pygame.display.flip()
        clock.tick(settings.FPS)

if __name__ == "__main__":
    main()
