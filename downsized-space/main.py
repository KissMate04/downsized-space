# pylint: disable=import-error, no-member
"""
Contains the game loop, levels and the menu.
"""
import sys
import os
import pygame
import game

class ShipPanels:
    def __init__(self, sw,sh):
        self.left_panel = pygame.image.load(
            os.path.join('sprites', "leftpanel.png")).convert_alpha()
        self.left_panel = pygame.transform.scale(
        self.left_panel, (sw, sh))
        self.right_panel = pygame.image.load(
            os.path.join('sprites', "rightpanel.png")).convert_alpha()
        self.right_panel = pygame.transform.scale(
            self.right_panel, (sw, sh))
        self.area_panel = pygame.image.load(
            os.path.join('sprites', "areapanel.png")).convert_alpha()
        self.area_panel = pygame.transform.scale(
            self.area_panel, (800, sh))

def main():
    current_scene = "main_menu"
    pygame.font.init()

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
    GAME_WIDTH = 800  # width of the game area
    SIDE_WIDTH = (SCREEN_WIDTH - GAME_WIDTH) // 2  # width of each side area
    GAME_AREA = pygame.Rect(
        SIDE_WIDTH,
        20,
        GAME_WIDTH,
        SCREEN_HEIGHT - 40
    )

    print(screen.get_size(), ", ", SIDE_WIDTH, ", ", GAME_AREA)

    def make_scene(name):
        if name == "main_menu":
            return game.MainScreen(GAME_AREA)
        if name == "level1":
            return game.LevelScene(GAME_AREA, LEVEL1, 1, ShipPanels(SIDE_WIDTH, SCREEN_HEIGHT))
        if name == "level2":
            return game.LevelScene(GAME_AREA, LEVEL2, 2, ShipPanels(SIDE_WIDTH, SCREEN_HEIGHT))
        if name == "level3":
            return game.LevelScene(GAME_AREA, LEVEL3, 3, ShipPanels(SIDE_WIDTH, SCREEN_HEIGHT))
        if name == "over":
            return game.GameOverScreen(GAME_AREA)
        return game.MainScreen(GAME_AREA)

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
        clock.tick(game.FPS)

if __name__ == "__main__":
    main()
