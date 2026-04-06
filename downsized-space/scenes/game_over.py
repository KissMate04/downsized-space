import pygame
from .. import settings

class GameOverScreen:
    """
    Game Over screen that appears when the player loses the game. It displays the final score and provides options to return to the main menu or quit the game.
    """
    def __init__(self):
        """
            Initializes the gamne over screen. It creates the buttons and the text for the buttons.
        """
        self.screen = settings.screen
        self.area = settings.GAME_AREA

        self.game_over_text = settings.game_over_font.render("GAME OVER", True, (255, 0, 0))
        self.score_text = settings.menu_font.render(f"Score: {settings.score}", True, (255, 255, 255))

        self.menu_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height // 11 * 7 - 50, 200, 100)
        self.menu_text = settings.menu_font.render("Main Menu", True, (255, 255, 255))

        self.quit_btn = pygame.Rect(
            (self.area.left + self.area.width // 2 - 100,
             self.area.height // 11 * 9 - 50 , 200, 100))
        self.quit_text = settings.menu_font.render("Quit", True, (255, 255, 255))
        pygame.mouse.set_visible(True)

    def handle_events(self, events):
        if self.menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return ["main_menu",0]

        if self.quit_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return ["QUIT",0]
        return ["over",0]

    def update(self, events):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(
            self.game_over_text,
            (self.quit_btn.centerx - self.game_over_text.get_width() // 2,
             self.screen.get_height() // 11 * 2)
        )
        self.screen.blit(
            self.score_text,
            (self.quit_btn.centerx - self.score_text.get_width() // 2,
             self.screen.get_height() // 11 * 5 - self.game_over_text.get_height() // 2)
        )
        self.screen.blit(
            self.menu_text,
            (self.menu_btn.centerx - self.menu_text.get_width() // 2,
             self.menu_btn.centery)
        )
        self.screen.blit(
            self.quit_text,
            (self.quit_btn.centerx - self.quit_text.get_width() // 2,
             self.quit_btn.centery)
        )
