import pygame
from ..entities.player import Player
from ..entities.projectile import Projectile
from ..entities.enemy import Enemy
from ..entities.boss import Boss

class LevelScene:
    """
    Class for the levels of the game. Each level has the same logic, but with different number of enemies.
    """
    def __init__(self, game_parameters, game_state, assets):
        """
        Initializes the level with the given number and enemy positions. Creates player and enemy objets, sets up the game area and pause menu.
        :param level: list of tuples with enemy positions in the format (nx, ny) where nx and ny are between 0 and 1 and represent the position of the enemy in the enemy area as a percentage.
        :param num: level number.
        """
        self.game_parameters = game_parameters
        self.game_state = game_state
        self.assets = assets
        # On level 1, two enemies will spawn, then two more on each level until we run out of spawn points.
        # Then one more boss will spawn on each level.
        self.level = self.game_parameters.spawn_points[0:min(len(game_parameters.spawn_points), game_state.level_num * 2)]

        # level start text
        self.level_text = self.assets.level_font.render(
            f"LEVEL {self.game_state.level_num}", True, (255, 10, 10))
        self.start_time = pygame.time.get_ticks()
        self.started = False  # to show level start text only once

        self.enemies = []
        for nx,ny in self.level:
            self.add_enemy(nx,ny)
        if self.game_state.level_num >= 6:
            for i in range(self.game_state.level_num-5):
                self.add_boss()

        self.projectiles = []
        self.p = Player(
            game_state.current_health,
            game_parameters.player_base_damage,
            game_parameters.player_speed,
            self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - 16,
            self.game_parameters.game_area.height - self.game_parameters.game_area.height // 4,
        self.game_parameters, self.assets)

        #pause menu buttons
        self.cont_text = assets.menu_font.render("Continue", True, (255, 255, 255))
        self.cont_btn = pygame.Rect(
                self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.cont_text.get_width() // 2,
                self.game_parameters.game_area.height // 3 - 50, self.cont_text.get_width(), self.cont_text.get_height())

        self.menu_text = assets.menu_font.render("Back to Main Menu", True, (255, 255, 255))
        self.menu_btn = pygame.Rect(
            self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.menu_text.get_width() // 2,
            self.game_parameters.game_area.height // 2 - 50, self.menu_text.get_width(), self.menu_text.get_height())

        self.quit_text = assets.menu_font.render("Quit", True, (255, 255, 255))
        self.quit_btn = pygame.Rect(
            (self.game_parameters.game_area.left + self.game_parameters.game_area.width // 2 - self.quit_text.get_width() // 2),
             self.game_parameters.game_area.height - self.game_parameters.game_area.height // 3, self.quit_text.get_width(), self.quit_text.get_height())

        self.menu_blit_sequence = [
            (self.cont_text, (self.cont_btn.centerx - self.cont_text.get_width() // 2,
                               self.cont_btn.centery - self.cont_text.get_height() // 2)),
            (self.menu_text, (self.menu_btn.centerx - self.menu_text.get_width() // 2,
                              self.menu_btn.centery - self.menu_text.get_height() // 2)),
            (self.quit_text, (self.quit_btn.centerx - self.quit_text.get_width() // 2,
                              self.quit_btn.centery - self.quit_text.get_height() // 2))
        ]

        # health and size bars
        # Yes these number are horrendous, i know
        self.health_bar_bg = pygame.Rect(self.game_parameters.side_width * 0.09, 20, self.game_parameters.side_width // 1.35, self.game_parameters.screen_height-20)
        self.health_bar = self.health_bar_bg.copy()
        self.size_bar_bg = pygame.Rect(
            self.game_parameters.side_width + self.game_parameters.game_area.width + self.game_parameters.side_width * 0.7,
            self.game_parameters.game_area.height * 0.4,
            self.game_parameters.side_width + self.game_parameters.game_area.width + self.game_parameters.side_width * 0.87 - self.game_parameters.side_width + self.game_parameters.game_area.width + self.game_parameters.side_width * 0.75,
            self.game_parameters.game_area.height - self.game_parameters.game_area.height * 0.4)
        self.size_bar = self.size_bar_bg.copy()
        self.size_bar_resize()
        self.health_bar_resize()

        pygame.mouse.set_visible(False)
        self.first_frame = True
        self.paused = False
        self.shooting = False

    def size_bar_resize(self):
        new_h = int(self.size_bar_bg.height * (self.p.shipsize / self.p.max_size))
        new_h = max(0, new_h)

        self.size_bar.height = new_h
        self.size_bar.top = self.size_bar_bg.bottom - new_h

    def health_bar_resize(self):
        self.health_bar.width = self.health_bar_bg.width * (self.p.health / self.game_state.starting_health)

    def add_enemy(self, nx,ny):
        x = int(self.game_parameters.enemy_area.left + nx * self.game_parameters.enemy_area.width)
        y = int(self.game_parameters.enemy_area.top + ny * self.game_parameters.enemy_area.height)

        self.enemies.append(
            Enemy(
                self.game_parameters.enemy_max_health,
                self.game_parameters.enemy_base_damage,
                self.game_parameters.enemy_speed,
                x,y,self.game_parameters, self.assets))
        # Bottom row spawns too low, so move them up a bit
        if y > self.game_parameters.enemy_area.height * 0.75:
            self.enemies[-1].y -= self.enemies[-1].shipsize

    def add_boss(self):
        self.enemies.append(
            Boss(
                self.game_parameters.boss_max_health,
                self.game_parameters.boss_base_damage,
                self.game_parameters.boss_speed,
                int(self.game_parameters.enemy_area.left + self.game_parameters.enemy_area.width // 2),
                int(self.game_parameters.enemy_area.top + self.game_parameters.enemy_area.height // 2),
                    self.game_parameters, self.assets)
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                pygame.mouse.set_visible(self.paused)
            if event.type == self.game_parameters.player_death:
                return "over"
            # track mouse hold state for continuous shooting
            if ((event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)):
                self.shooting = True
            if ((event.type == pygame.MOUSEBUTTONUP and event.button == 1) or
                    (event.type == pygame.KEYUP and event.key == pygame.K_SPACE)):
                self.shooting = False
            # Resizing player with mousewheel
            if event.type == pygame.MOUSEWHEEL:
                self.p.resize(event.y)
                self.size_bar_resize()
            # Enemy shooting automatically
            if event.type == self.game_parameters.enemy_shot:
                for en in self.enemies:
                    if en.shoot():
                        self.projectiles.append(
                            Projectile(
                                en.x + en.shipsize / 2,
                                en.y + en.shipsize,
                                en.shipsize / 2,
                                self.game_parameters.projectile_speed,
                                en.damage,
                                en))

        if self.paused:
            if self.cont_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                pygame.mouse.set_visible(False)
                self.paused = False
            if self.menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                return "main_menu"
            if self.quit_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                return "QUIT"
        if not self.enemies:
            self.game_state.score += 100
            self.game_state.current_health = self.p.health
            self.game_state.level_num += 1
            return "level"
        return "level"

    def update(self, events):
        if self.paused:
            return
        if self.first_frame:
            self.first_frame = False
            return

        # Shows level number for 2 seconds at the start of the level
        if not self.started:
            if pygame.time.get_ticks() - self.start_time > 2000:
                self.started = True

        #remove dead enemies
        self.enemies = [e for e in self.enemies if e.alive]

        # Move enemies
        for en in self.enemies:
            en.move()

        # Player shooting with left mouse click or space
        if self.shooting:
            self.player_shooting()

        self.projectile_movement()

        # Player movement
        keys = pygame.key.get_pressed()
        if any(
                keys[key] for key in [
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                    pygame.K_UP,
                    pygame.K_DOWN,
                    pygame.K_w,
                    pygame.K_a,
                    pygame.K_s,
                    pygame.K_d]):
            self.p.move(keys)

    def player_shooting(self):
        if self.p.shoot():
            self.projectiles.append(
                Projectile(
                    self.p.x + self.p.shipsize / 2,
                    self.p.y, self.p.shipsize / 2,
                    self.game_parameters.projectile_speed,
                    self.p.damage,
                    self.p)
            )
            self.assets.sounds["player_shot"].play()

    def projectile_movement(self):
        for proj in self.projectiles:
            proj.move()
            # Check projectile for collision with enemies
            # remove projectile and damage the enemy
            if str(proj.shooter) == "Player":
                for en in self.enemies:
                    if proj.hitbox.colliderect(en.hitbox):
                        if not en.dying:
                            if en.hit(proj.damage) is not None:
                                self.game_state.score += en.value
                        if proj in self.projectiles:
                            self.projectiles.remove(proj)
                        break

            else:
                # Check projectile for collision with player
                # if hit damage the player, remove projectile and promote the shooter
                if proj.hitbox.colliderect(self.p.hitbox):
                    self.p.hit(proj.damage)
                    proj.shooter.promotion()
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    self.health_bar_resize()

                # Remove projectile if it goes off-screen
                if proj in self.projectiles and (
                        proj.y < 0 or proj.y > self.game_parameters.screen_height):
                    self.projectiles.remove(proj)

    def draw(self):
        if self.paused:
            self.game_parameters.screen.blits(self.menu_blit_sequence)
            return

        self.game_parameters.screen.fill((50, 50, 50))
        pygame.draw.rect(self.game_parameters.screen, (255, 0, 0), self.health_bar_bg)
        pygame.draw.rect(self.game_parameters.screen, (0, 255, 0), self.health_bar)
        pygame.draw.rect(self.game_parameters.screen, (180, 230, 255), self.size_bar_bg)
        pygame.draw.rect(self.game_parameters.screen, (235, 180, 52), self.size_bar)
        self.game_parameters.screen.blit(self.assets.left_panel, (0, 0))
        self.game_parameters.screen.blit(self.assets.area_panel, (self.game_parameters.side_width, 0))
        self.game_parameters.screen.blit(self.assets.right_panel, (self.game_parameters.side_width + self.game_parameters.game_width, 0))

        if not self.started:
            self.game_parameters.screen.blit(
                self.level_text,
                (self.game_parameters.screen.get_width() / 2 - self.level_text.get_width() / 2,
                 self.game_parameters.screen.get_height() / 2 - self.level_text.get_height() / 2))

        self.game_parameters.screen.blit(self.p.image, (self.p.x, self.p.y))
        for en in self.enemies:
            self.game_parameters.screen.blit(en.image, (en.x, en.y))
        for proj in self.projectiles:
            proj.draw(self.game_parameters.screen)
