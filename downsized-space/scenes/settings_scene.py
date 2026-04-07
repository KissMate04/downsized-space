from .. import settings
import pygame
import os

class SettingsScreen:
    """
    Class for the settings scene. Can only be accessed from the main menu for now.
    """
    def __init__(self):
        """
        Initialize the settings scene.
        """
        self.screen = settings.screen
        self.area = settings.GAME_AREA

        self.music_settings_text = settings.menu_font.render("Music: ", True, (255, 255, 255))
        self.music_settings_value = settings.menu_font.render(str(int(settings.MUSIC_VOLUME*10)), True, (255, 255, 255))
        self.music_settings_btn_left = pygame.Rect(pygame.Rect(
            self.area.left + self.area.width,
            self.area.height // 4 - self.music_settings_value.get_height() // 2, self.music_settings_value.get_height(), self.music_settings_value.get_height()))
        self.music_settings_btn_right = pygame.Rect(pygame.Rect(
            self.area.left + self.area.width + self.music_settings_btn_left.width*4,
            self.area.height // 4 - self.music_settings_value.get_height() // 2, self.music_settings_value.get_height(), self.music_settings_value.get_height()))

        self.sounds_settings_text = settings.menu_font.render("Sounds: ", True, (255, 255, 255))
        self.sounds_settings_value = settings.menu_font.render(str(int(settings.SOUNDS_VOLUME*10)), True, (255, 255, 255))
        self.sounds_settings_btn_left = pygame.Rect(pygame.Rect(
            self.area.left + self.area.width,
            self.area.height // 2 - self.music_settings_value.get_height() // 2, self.music_settings_value.get_height(), self.music_settings_value.get_height()))
        self.sounds_settings_btn_right = pygame.Rect(pygame.Rect(
            self.area.left + self.area.width+ self.music_settings_btn_left.width*4,
            self.area.height // 2 - self.music_settings_value.get_height() // 2, self.music_settings_value.get_height(), self.music_settings_value.get_height()))

        self.settings_btn_left_image = pygame.image.load(os.path.join('downsized-space',"sprites", "settings_btn_left.png")).convert_alpha()
        self.settings_btn_left_image = pygame.transform.scale(
            self.settings_btn_left_image, (self.music_settings_value.get_height(), self.music_settings_value.get_height()))
        self.settings_btn_right_image = pygame.image.load(os.path.join('downsized-space',"sprites", "settings_btn_right.png")).convert_alpha()
        self.settings_btn_right_image = pygame.transform.scale(
            self.settings_btn_right_image, (self.music_settings_value.get_height(), self.music_settings_value.get_height()))

        self.menu_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height // 4 * 3 - 50, 200, 100)
        self.menu_text = settings.menu_font.render("Back", True, (255, 255, 255))
        self.test = settings.menu_font.render("hover detected", True, (255, 255, 255))
        self.istest = False
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.music_settings_btn_left.collidepoint(pygame.mouse.get_pos()):
                    settings.MUSIC_VOLUME = max(0.0, round(settings.MUSIC_VOLUME - 0.1,1))
                    pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
                    self.music_settings_value = settings.menu_font.render(str(int(settings.MUSIC_VOLUME*10)), True, (255, 255, 255))

                if self.music_settings_btn_right.collidepoint(pygame.mouse.get_pos()):
                    settings.MUSIC_VOLUME = min(1.0, round(settings.MUSIC_VOLUME + 0.1,1))
                    pygame.mixer.music.set_volume(settings.MUSIC_VOLUME)
                    self.music_settings_value = settings.menu_font.render(str(int(settings.MUSIC_VOLUME * 10)), True, (255, 255, 255))

                if self.sounds_settings_btn_left.collidepoint(pygame.mouse.get_pos()):
                    settings.SOUNDS_VOLUME = max(0.0, round(settings.SOUNDS_VOLUME - 0.1,1))
                    for each in settings.sounds:
                        settings.sounds[each].set_volume(settings.SOUNDS_VOLUME)
                    self.sounds_settings_value = settings.menu_font.render(str(int(settings.SOUNDS_VOLUME*10)), True, (255, 255, 255))
                    settings.sounds["player_shot"].play()

                if self.sounds_settings_btn_right.collidepoint(pygame.mouse.get_pos()):
                    settings.SOUNDS_VOLUME = min(1.0, round(settings.SOUNDS_VOLUME + 0.1,1))
                    for each in settings.sounds:
                        settings.sounds[each].set_volume(settings.SOUNDS_VOLUME)
                    self.sounds_settings_value = settings.menu_font.render(str(int(settings.SOUNDS_VOLUME*10)), True, (255, 255, 255))
                    settings.sounds["player_shot"].play()

                if self.menu_btn.collidepoint(pygame.mouse.get_pos()):
                        return ["main_menu", 0]

        return ["settings", 0]

    def update(self, events):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(
            self.music_settings_text,
            (self.area.left,
            #(self.area.left + self.area.width // 2 - self.sounds_settings_text.get_width() // 2,
             self.area.height // 4 - self.music_settings_text.get_height() // 2)
        )
        self.screen.blit(
            self.settings_btn_left_image,
            self.music_settings_btn_left
        )
        self.screen.blit(
            self.music_settings_value,
            (self.area.left + self.area.width + self.music_settings_btn_left.width*2,
             self.area.height // 4 - self.music_settings_value.get_height() // 2)
        )
        self.screen.blit(
            self.settings_btn_right_image,
            self.music_settings_btn_right
        )
        self.screen.blit(
            self.sounds_settings_text,
            (self.area.left,
            #(self.area.left + self.area.width // 2 - self.sounds_settings_text.get_width() // 2,
             self.area.height // 2 - self.sounds_settings_text.get_height() // 2)
        )
        self.screen.blit(
            self.settings_btn_left_image,
            self.sounds_settings_btn_left
        )
        self.screen.blit(
            self.sounds_settings_value,
            (self.area.left + self.area.width + self.music_settings_btn_left.width*2,
             self.area.height // 2 - self.sounds_settings_value.get_height() // 2)
        )
        self.screen.blit(
            self.settings_btn_right_image,
            self.sounds_settings_btn_right
        )

        self.screen.blit(
            self.menu_text,
            (self.menu_btn.centerx - self.menu_text.get_width() // 2,
             self.menu_btn.centery - self.menu_text.get_height() // 2)
        )
