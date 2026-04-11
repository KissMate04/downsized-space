# Current problems:
# random lag spikes?
# movement sometimes faster
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
from. import game_state
from. import asset_manager

def make_scene( gp : settings.Settings, gs :  game_state.GameState, ass : asset_manager.AssetManager):
    """
    Returns an instance of the next scene's class.
    One of the following: MainScreen, SettingsScreen, LevelScene, GameOverScreen.
    :param gp: Used to get the spawn points, then given to the next scene as parameter.
    :param gs: Used to get the current scene name and level number, then given to the next scene as parameter.
    :param ass: Used to load and unload the music, then given to the next scene as parameter.
    :return:
    """
    if gs.current_scene_name == "main_menu":
        pygame.time.wait(250)  # to avoid clicking from the previous scene effecting the menu
        ass.load_music("music_menu.wav")
        pygame.mixer.music.play(-1)
        return MainScreen(gp,gs,ass)
    if gs.current_scene_name == "settings":
        pygame.time.wait(250)  # to avoid clicking from the previous scene effecting the menu
        return SettingsScreen(gp,gs,ass)
    if gs.current_scene_name == "level":
        if gs.level_num < 2:  # This allows continuous music playing between levels
            ass.load_music("music_game.wav")
            pygame.mixer.music.play(-1)
        # On level 1, two enemies will spawn, then two more on each level until we run out of spawn points.
        # Then one more boss will spawn on each level.
        return LevelScene(gp,gs,ass)
    if gs.current_scene_name == "over":
        ass.unload_music()
        return GameOverScreen(gp,gs,ass)
    return MainScreen(gp,gs,ass)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    #dificulty will be added later.
    game_parameters = settings.Settings(screen, player_max_health=100, player_base_damage=53, enemy_max_health=100,enemy_base_damage=30,enemy_speed=3.5,enemy_shot_timer=800,boss_max_health=250,boss_base_damage=50,boss_speed=4,projectile_speed=6)
    state = game_state.GameState("main_menu", game_parameters.player_max_health)
    assets = asset_manager.AssetManager(game_parameters.side_width, game_parameters.screen_height, game_parameters.game_width)

    current_scene = make_scene(game_parameters,state,assets)
    current_level_num = state.level_num

    while True:
        events = pygame.event.get()
        if any(event.type == pygame.QUIT for event in events):
            pygame.quit()
            sys.exit()

        next_scene = current_scene.handle_events(events)

        if next_scene == "QUIT":
            pygame.quit()
            sys.exit()

        if next_scene != state.current_scene_name or current_level_num != state.level_num:
            state.current_scene_name = next_scene
            if state.current_scene_name == "main_menu":
                state.level_num = 0
            current_level_num = state.level_num
            current_scene = make_scene(game_parameters,state,assets)
        current_scene.update(events)
        current_scene.draw()

        pygame.display.flip()
        clock.tick(game_parameters.fps)

if __name__ == "__main__":
    main()
