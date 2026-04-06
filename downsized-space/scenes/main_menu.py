import pygame
from .. import settings

class MainScreen:
    """
    Class for the main menu screen of the game. This is the first screen.
    It has Start, Settings, How to Play and Quit buttons.
    """
    def __init__(self):
        """
        Initializes the main menu screen. It creates the buttons and the text for the buttons.
        """
        self.screen = settings.screen
        self.area = settings.GAME_AREA

        # Positioning: The screen is divided into 11 horizontal sections. The buttons are placed in the 3rd, 5th and 7th sections.
        self.start_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height // 11 * 3 - 50, 200, 100)
        self.start_text = settings.menu_font.render("Start", True, (255, 255, 255))

        self.settings_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height // 11 * 5 - 50, 200, 100)
        self.settings_text = settings.menu_font.render("Settings", True, (255, 255, 255))

        self.howto_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height // 11 * 7 -50, 200, 100)
        # text inside how to menu. Positioning: The screen is divided into 12 horizontal sections. The text is placed in the 3rd, 4th, 6th, 8th and 10th sections.
        self.howto_text = settings.menu_font.render("How To Play", True, (255, 255, 255))
        self.howto_text_scroll = settings.menu_font.render("Scroll with your mouse to change size.", True, (255, 255, 255))
        self.howto_text_enemy = settings.menu_font.render("The bigger your ship, the more damage you deal!", True, (255, 255, 255))
        self.howto_text_move = settings.menu_font.render("Use WASD or arrow keys to move your ship.", True, (255, 255, 255))
        self.howto_text_shoot = settings.menu_font.render("Click left mouse button or press space to shoot.", True, (255, 255, 255))
        self.back_to_menu_text = settings.menu_font.render("Got it!", True, (255, 255, 255))
        self.back_to_menu_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height // 12 * 10 - 50, 200, 100)

        self.quit_btn = pygame.Rect(
            (self.area.left + self.area.width // 2 - 100,
             self.area.height // 11 * 9 - 50, 200, 100))
        self.quit_text = settings.menu_font.render("Quit", True, (255, 255, 255))
        self.is_howto = False

    def handle_events(self, events):
        if self.is_howto:
            if self.back_to_menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.is_howto = False
                pygame.time.wait(240) # to avoid clicking from the previous scene effecting the menu
        else:
            if self.start_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                settings.score = 0
                return ["level",1]

            if self.howto_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.is_howto = True

            if self.quit_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                return ["QUIT",0]
        return ["main_menu",0]

    def update(self, events):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        # Show how to play text.
        if self.is_howto:
            self.screen.blit(
                self.howto_text_scroll,
                (self.area.left + self.area.width // 2 - self.howto_text_scroll.get_width() // 2,
                 self.area.height // 12 * 3 - self.howto_text_scroll.get_height() // 2)
            )
            self.screen.blit(
                self.howto_text_enemy,
                (self.area.left + self.area.width // 2 - self.howto_text_enemy.get_width() // 2,
                 self.area.height // 12 * 4 - self.howto_text_scroll.get_height() // 2)
            )
            self.screen.blit(
                self.howto_text_move,
                (self.area.left + self.area.width // 2 - self.howto_text_move.get_width() // 2,
                 self.area.height // 12 * 6 - self.howto_text_scroll.get_height() // 2)
            )
            self.screen.blit(
                self.howto_text_shoot,
                (self.area.left + self.area.width // 2 - self.howto_text_shoot.get_width() // 2,
                 self.area.height // 12 * 8 - self.howto_text_move.get_height() // 2)
            )
            self.screen.blit(
                self.back_to_menu_text,
                (self.back_to_menu_btn.centerx - self.back_to_menu_text.get_width() // 2,
                 self.back_to_menu_btn.centery)
            )
        else:
            # Show normal menu
            self.screen.blit(
                self.start_text,
                (self.start_btn.centerx - self.start_text.get_width() // 2,
                self.start_btn.centery)
            )
            self.screen.blit(
                self.settings_text,
                (self.settings_btn.centerx - self.settings_text.get_width() // 2,
                 self.settings_btn.centery)
            )
            self.screen.blit(
                self.howto_text,
                (self.howto_btn.centerx - self.howto_text.get_width() // 2,
                 self.howto_btn.centery)
            )
            self.screen.blit(
                self.quit_text,
                (self.quit_btn.centerx - self.quit_text.get_width() // 2,
                 self.quit_btn.centery)
            )
