from .. import settings
import pygame
import os

class SettingsScreen:
    """
    Class for the settings scene. Can only be accessed from the main menu for now.
    """
    def __init__(self, game_parameters, game_state, assets):
        """
        Initialize the settings scene.
        """
        self.game_parameters = game_parameters
        self.game_state = game_state
        self.assets = assets

        self.music_settings_text = self.assets.menu_font.render("Music: ", True, (255, 255, 255))
        self.music_settings_value = self.assets.menu_font.render(str(int(self.game_state.music_volume*10)), True, (255, 255, 255))
        self.music_settings_btn_left = pygame.Rect(pygame.Rect(
            self.game_parameters.game_area.left + self.game_parameters.game_area.width,
            self.game_parameters.game_area.height // 4 - self.music_settings_value.get_height() // 2, self.music_settings_value.get_height(), self.music_settings_value.get_height()))
        self.music_settings_btn_right = pygame.Rect(pygame.Rect(
            self.game_parameters.game_area.left + self.game_parameters.game_area.width + self.music_settings_btn_left.width*4,
            self.game_parameters.game_area.height // 4 - self.music_settings_value.get_height() // 2, self.music_settings_value.get_height(), self.music_settings_value.get_height()))

        self.sounds_settings_text = self.assets.menu_font.render("Sounds: ", True, (255, 255, 255))
        self.sounds_settings_value = self.assets.menu_font.render(str(int(self.game_state.sound_volume*10)), True, (255, 255, 255))
        self.sounds_settings_btn_left = pygame.Rect(pygame.Rect(
            self.game_parameters.game_area.left + self.game_parameters.game_area.width,
            self.game_parameters.game_area.height // 2 - self.music_settings_value.get_height() // 2, self.music_settings_value.get_height(), self.music_settings_value.get_height()))
        self.sounds_settings_btn_right = pygame.Rect(pygame.Rect(
            self.game_parameters.game_area.left + self.game_parameters.game_area.width+ self.music_settings_btn_left.width*4,
            self.game_parameters.game_area.height // 2 - self.music_settings_value.get_height() // 2, self.music_settings_value.get_height(), self.music_settings_value.get_height()))

        self.settings_btn_left_image = self.assets.load_sprite("settings_btn_left.png", self.music_settings_value.get_height(), self.music_settings_value.get_height())
        self.settings_btn_right_image = self.assets.load_sprite("settings_btn_right.png", self.music_settings_value.get_height(), self.music_settings_value.get_height())

        self.menu_text = self.assets.menu_font.render("Back", True, (255, 255, 255))
        self.menu_btn = pygame.Rect(
            self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.menu_text.get_width() // 2,
            self.game_parameters.game_area.height // 4 * 3 - 50, self.menu_text.get_width(), self.menu_text.get_height())

        self.menu_blit_sequence = [
            (self.music_settings_text,
             (self.game_parameters.game_area.left,
              self.game_parameters.game_area.height // 4 - self.music_settings_text.get_height() // 2)),

            (self.settings_btn_left_image, self.music_settings_btn_left), # I JUST GAVE IT THE RECT! IF SOMETHING BREAKS IT'S BECAUSE OF THIS
            (self.settings_btn_right_image, self.music_settings_btn_right),
            (self.sounds_settings_text,
             (self.game_parameters.game_area.left,
             self.game_parameters.game_area.height // 2 - self.sounds_settings_text.get_height() // 2)),

            (self.settings_btn_left_image, self.sounds_settings_btn_left),
            (self.settings_btn_right_image, self.sounds_settings_btn_right),
            (self.menu_text,
             self.menu_btn)
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.music_settings_btn_left.collidepoint(pygame.mouse.get_pos()):
                    self.game_state.music_volume = max(0.0, round(self.game_state.music_volume - 0.1,1))
                    pygame.mixer.music.set_volume(self.game_state.music_volume)
                    self.music_settings_value = self.assets.menu_font.render(str(int(self.game_state.music_volume*10)), True, (255, 255, 255))

                if self.music_settings_btn_right.collidepoint(pygame.mouse.get_pos()):
                    self.game_state.music_volume = min(1.0, round(self.game_state.music_volume + 0.1,1))
                    pygame.mixer.music.set_volume(self.game_state.music_volume)
                    self.music_settings_value = self.assets.menu_font.render(str(int(self.game_state.music_volume * 10)), True, (255, 255, 255))

                if self.sounds_settings_btn_left.collidepoint(pygame.mouse.get_pos()):
                    self.game_state.sound_volume = max(0.0, round(self.game_state.sound_volume - 0.1,1))
                    for each in self.assets.sounds:
                        self.assets.sounds[each].set_volume(self.game_state.sound_volume)
                    self.sounds_settings_value = self.assets.menu_font.render(str(int(self.game_state.sound_volume*10)), True, (255, 255, 255))
                    self.assets.sounds["player_shot"].play()

                if self.sounds_settings_btn_right.collidepoint(pygame.mouse.get_pos()):
                    self.game_state.sound_volume = min(1.0, round(self.game_state.sound_volume + 0.1,1))
                    for each in self.assets.sounds:
                        self.assets.sounds[each].set_volume(self.game_state.sound_volume)
                    self.sounds_settings_value = self.assets.menu_font.render(str(int(self.game_state.sound_volume*10)), True, (255, 255, 255))
                    self.assets.sounds["player_shot"].play()

                if self.menu_btn.collidepoint(pygame.mouse.get_pos()):
                        return "main_menu"

        return "settings"

    def update(self, events):
        pass

    def draw(self):
        self.game_parameters.screen.fill((0, 0, 0))
        self.game_parameters.screen.blits(self.menu_blit_sequence)
        self.game_parameters.screen.blit(self.music_settings_value,
         (self.game_parameters.game_area.left + self.game_parameters.game_area.width + self.music_settings_btn_left.width * 2,
          self.game_parameters.game_area.height // 4 - self.music_settings_value.get_height() // 2))
        self.game_parameters.screen.blit(self.sounds_settings_value,
         (self.game_parameters.game_area.left + self.game_parameters.game_area.width + self.music_settings_btn_left.width * 2,
          self.game_parameters.game_area.height // 2 - self.sounds_settings_value.get_height() // 2))