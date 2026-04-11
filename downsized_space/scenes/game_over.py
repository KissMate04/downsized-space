import pygame

class GameOverScreen:
    """
    Game Over screen that appears when the player loses the game. It displays the final score and provides options to return to the main menu or quit the game.
    """
    def __init__(self, game_parameters, game_state, assets):
        """
            Initializes the gamne over screen. It creates the buttons and the text for the buttons.
        """
        self.game_parameters = game_parameters
        self.game_state = game_state
        self.assets = assets

        self.game_over_text = assets.game_over_font.render("GAME OVER", True, (255, 0, 0))
        self.score_text = assets.menu_font.render(f"Score: {game_state.score}", True, (255, 255, 255))

        self.menu_text = assets.menu_font.render("Main Menu", True, (255, 255, 255))
        self.menu_btn = pygame.Rect(
            self.game_parameters.side_width + self.game_parameters.game_width // 2 - self.menu_text.get_width() // 2,
            self.game_parameters.game_area.height // 11 * 7 - 50, self.menu_text.get_width(), self.menu_text.get_height())

        self.quit_text = assets.menu_font.render("Quit", True, (255, 255, 255))
        self.quit_btn = pygame.Rect(
            self.game_parameters.side_width + self.game_parameters.game_width // 2 - self.quit_text.get_width() // 2,
             self.game_parameters.game_area.height // 11 * 9 - 50 , self.quit_text.get_width(), self.quit_text.get_height())


        self.menu_blit_sequence = [
            (self.game_over_text,
             (self.quit_btn.centerx - self.game_over_text.get_width() // 2,
              self.game_parameters.screen_height // 11 * 2)),
            (self.score_text,
             (self.quit_btn.centerx - self.score_text.get_width() // 2,
              self.game_parameters.screen_height // 11 * 5 - self.game_over_text.get_height() // 2)),
            (self.menu_text, self.menu_btn),
            (self.quit_text, self.quit_btn)
        ]
        pygame.mouse.set_visible(True)

    def handle_events(self, events):
        if self.menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return "main_menu"

        if self.quit_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return "QUIT"
        return "over"

    def update(self, events):
        pass

    def draw(self):
        self.game_parameters.screen.fill((0, 0, 0))
        self.game_parameters.screen.blits(self.menu_blit_sequence)
