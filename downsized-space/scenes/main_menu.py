import pygame
from .. import settings

class MainScreen:
    def __init__(self):
        self.screen = settings.screen
        self.area = settings.GAME_AREA
        self.start_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height // 3 - 80, 200, 100)

        self.start_text = settings.menu_font.render("Start", True, (255, 255, 255))

        self.howto_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height // 2 - 30, 200, 100)
        self.howto_text = settings.menu_font.render("How To Play", True, (255, 255, 255))
        self.howto_text_scroll = settings.menu_font.render("Scroll with your mouse to change size.", True, (255, 255, 255))
        self.howto_text_enemy = settings.menu_font.render("The bigger your ship, the more damage you deal!", True, (255, 255, 255))
        self.howto_text_move = settings.menu_font.render("Use WASD or arrow keys to move your ship.", True, (255, 255, 255))
        self.howto_text_shoot = settings.menu_font.render("Click left mouse button or press space to shoot.", True, (255, 255, 255))
        self.back_to_menu_text = settings.menu_font.render("Got it!", True, (255, 255, 255))
        self.back_to_menu_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height - self.area.height // 5, 200, 100)

        self.quit_btn = pygame.Rect(
            (self.area.left + self.area.width // 2 - 100,
             self.area.height - self.area.height // 3 + 30, 200, 100))
        self.quit_text = settings.menu_font.render("Quit", True, (255, 255, 255))
        self.is_howto = False

    def handle_events(self, events):
        if not self.is_howto and self.start_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return ["level",1]

        if not self.is_howto and self.howto_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.is_howto = not self.is_howto

        if not self.is_howto and self.quit_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return ["QUIT",0]

        if self.is_howto and self.back_to_menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            self.is_howto = False

        return ["main_menu",0]

    def update(self, events):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.is_howto:
            self.screen.blit(
                self.howto_text_scroll,
                (self.area.left + self.area.width // 2 - self.howto_text_scroll.get_width() // 2,
                 self.area.height // 6)
            )
            self.screen.blit(
                self.howto_text_enemy,
                (self.area.left + self.area.width // 2 - self.howto_text_enemy.get_width() // 2,
                 self.area.height // 6 + self.howto_text_scroll.get_height() * 2)
            )
            self.screen.blit(
                self.howto_text_move,
                (self.area.left + self.area.width // 2 - self.howto_text_move.get_width() // 2,
                 self.area.height // 6 + self.howto_text_scroll.get_height() * 6)
            )
            self.screen.blit(
                self.howto_text_shoot,
                (self.area.left + self.area.width // 2 - self.howto_text_shoot.get_width() // 2,
                 self.area.height // 6 + self.howto_text_move.get_height() * 10)
            )
            self.screen.blit(
                self.back_to_menu_text,
                (self.back_to_menu_btn.centerx - self.back_to_menu_text.get_width() // 2,
                 self.back_to_menu_btn.centery - self.back_to_menu_text.get_height() // 2)
            )
        else:
            self.screen.blit(
                self.start_text,
                (self.start_btn.centerx - self.start_text.get_width() // 2,
                self.start_btn.centery - self.start_text.get_height() // 2)
            )
            self.screen.blit(
                self.howto_text,
                (self.howto_btn.centerx - self.howto_text.get_width() // 2,
                 self.howto_btn.centery - self.howto_text.get_height() // 2)
            )
            self.screen.blit(
                self.quit_text,
                (self.quit_btn.centerx - self.quit_text.get_width() // 2,
                 self.quit_btn.centery - self.quit_text.get_height() // 2)
            )
