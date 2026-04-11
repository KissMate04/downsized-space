import pygame

class MainScreen:
    """
    Class for the main menu screen of the game. This is the first screen.
    It has Start, Settings, How to Play and Quit buttons.
    """
    def __init__(self, game_parameters, game_state, assets ):
        """
        Initializes the main menu screen. It creates the buttons and the text for the buttons.
        """
        self.game_parameters = game_parameters
        self.game_state = game_state
        self.assets = assets

        # Positioning: The screen is divided into 11 horizontal sections. The buttons are placed in the 3rd, 5th and 7th sections.
        self.start_text = assets.menu_font.render("Start", True, (255, 255, 255))
        self.start_btn = pygame.Rect(
            self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.start_text.get_width() // 2,
            self.game_parameters.game_area.height // 11 * 3, self.start_text.get_width(), self.start_text.get_height())

        self.settings_text = assets.menu_font.render("Settings", True, (255, 255, 255))
        self.settings_btn = pygame.Rect(
            self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.settings_text.get_width() // 2,
            self.game_parameters.game_area.height // 11 * 5, self.settings_text.get_width(), self.settings_text.get_height())

        self.howto_text = assets.menu_font.render("How To Play", True, (255, 255, 255))
        self.howto_btn = pygame.Rect(
            self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.howto_text.get_width() // 2,
            self.game_parameters.game_area.height // 11 * 7, self.howto_text.get_width(), self.howto_text.get_height())

        # text inside how to menu. Positioning: The screen is divided into 12 horizontal sections. The text is placed in the 3rd, 4th, 6th, 8th and 10th sections.
        self.howto_text_scroll = assets.menu_font.render("Scroll with your mouse to change size.", True,
                                                         (255, 255, 255))
        self.howto_text_scroll_pos = (self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.howto_text_scroll.get_width() // 2,
                      self.game_parameters.game_area.height // 12 * 3 - self.howto_text_scroll.get_height() // 2)

        self.howto_text_enemy = assets.menu_font.render("The bigger your ship, the more damage you deal!", True, (255, 255, 255))
        self.howto_text_enemy_pos =  (self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.howto_text_enemy.get_width() // 2,
                      self.game_parameters.game_area.height // 12 * 4 - self.howto_text_scroll.get_height() // 2)

        self.howto_text_move = assets.menu_font.render("Use WASD or arrow keys to move your ship.", True, (255, 255, 255))
        self.howto_text_move_pos = (self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.howto_text_move.get_width() // 2,
         self.game_parameters.game_area.height // 12 * 6 - self.howto_text_scroll.get_height() // 2)

        self.howto_text_shoot = assets.menu_font.render("Click left mouse button or press space to shoot.", True, (255, 255, 255))
        self.howto_text_shoot_pos = (self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.howto_text_shoot.get_width() // 2,
                       self.game_parameters.game_area.height // 12 * 8 - self.howto_text_move.get_height() // 2)

        self.got_it_text = assets.menu_font.render("Got it!", True, (255, 255, 255))
        self.got_it_btn = pygame.Rect(
            self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.got_it_text.get_width() // 2,
            self.game_parameters.game_area.height // 12 * 10, self.got_it_text.get_width(), self.got_it_text.get_height())

        self.quit_text = assets.menu_font.render("Quit", True, (255, 255, 255))
        self.quit_btn = pygame.Rect(
            (self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.quit_text.get_width() // 2,
             self.game_parameters.game_area.height // 11 * 9, self.quit_text.get_width(), self.quit_text.get_height()))

        self.howto_blit_sequence = [
            (self.howto_text_scroll, self.howto_text_scroll_pos),
            (self.howto_text_enemy, self.howto_text_enemy_pos),
            (self.howto_text_move, self.howto_text_move_pos),
            (self.howto_text_shoot, self.howto_text_shoot_pos),
            (self.got_it_text, self.got_it_btn)
        ]
        self.menu_blit_sequence = [
            (self.start_text, self.start_btn),
            (self.settings_text, self.settings_btn),
            (self.howto_text, self.howto_btn),
            (self.quit_text, self.quit_btn),
        ]

        self.is_howto = False

    def handle_events(self, events):
        if self.is_howto:
            if self.got_it_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.is_howto = False
                pygame.time.wait(250) # to avoid clicking from the previous scene effecting the menu
        else:
            if self.start_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.game_state.score = 0
                self.game_state.current_health = self.game_state.starting_health
                self.game_state.level_num = 1
                return "level"

            if self.settings_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                return "settings"

            if self.howto_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                self.is_howto = True

            if self.quit_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                return "QUIT"
        return "main_menu"

    def update(self, events):
        pass

    def draw(self):
        self.game_parameters.screen.fill((0, 0, 0))
        # Show how to play text.
        if self.is_howto:
            self.game_parameters.screen.blits(self.howto_blit_sequence)
        else:
            # Show normal menu
            self.game_parameters.screen.blits(self.menu_blit_sequence)
