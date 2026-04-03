import pygame
from ..entities.player import Player
from ..entities.projectile import Projectile
from ..entities.enemy import Enemy
from .. import settings

class LevelScene:
    def __init__(self, area, level, num, ship_panels):
        self.start_time = pygame.time.get_ticks()
        self.num = num # level number
        self.started = False # to show level start text only once
        self.area = area
        self.ship_panels = ship_panels
        self.paused = False
        self.enemies = []
        for nx,ny in level:
            self.add_enemy(nx,ny)
        self.projectiles = []
        self.p = Player(
            self.area.width,
            'startership.png',
            settings.PLAYER_MAX_HEALTH,
            settings.PLAYER_BASE_DAMAGE,
            settings.PLAYER_SPEED,
            self.area.left + self.area.width // 2 - 16,
            self.area.height - self.area.height // 4)
        #pause menu buttons
        self.cont_btn = pygame.Rect(
                self.area.left + self.area.width // 2 - 100,
                self.area.height // 3 - 50, 200, 100)
        self.cont_text = settings.menu_font.render("Continue", True, (255, 255, 255))
        self.quit_btn = pygame.Rect(
            (self.area.left + self.area.width // 2 - 100,
             self.area.height - self.area.height // 3, 200, 100))
        self.quit_text = settings.menu_font.render("Quit", True, (255, 255, 255))
        # level start text
        self.level_text = settings.level_font.render(
            f"LEVEL {self.num}", True, (255, 10, 10))
        pygame.mouse.set_visible(False)
        self.health_bar_bg = pygame.Rect(self.ship_panels.left_panel.get_width() * 0.09, 20, self.ship_panels.left_panel.get_width() // 1.35, self.area.height-20)
        self.health_bar = pygame.Rect(self.ship_panels.left_panel.get_width() * 0.09, 20, self.ship_panels.left_panel.get_width() // 1.35, self.area.height-20)
        self.size_bar_bg = pygame.Rect(
            self.ship_panels.left_panel.get_width() + self.area.width + self.ship_panels.right_panel.get_width() * 0.7,
            self.area.height * 0.44,
            self.ship_panels.left_panel.get_width() + self.area.width + self.ship_panels.right_panel.get_width() * 0.87 - self.ship_panels.left_panel.get_width() + self.area.width + self.ship_panels.right_panel.get_width() * 0.75,
            self.area.height * 0.96 - self.area.height * 0.4)
        self.size_bar = pygame.Rect(
            self.ship_panels.left_panel.get_width() + self.area.width + self.ship_panels.right_panel.get_width() * 0.7,
            self.area.height * 0.44,
            self.ship_panels.left_panel.get_width() + self.area.width + self.ship_panels.right_panel.get_width() * 0.87 - self.ship_panels.left_panel.get_width() + self.area.width + self.ship_panels.right_panel.get_width() * 0.75,
            self.area.height * 0.96 - self.area.height * 0.4)
        self.size_bar_resize()

    def size_bar_resize(self):
        new_h = int(self.size_bar_bg.height * (self.p.shipsize / self.p.max_size))
        new_h = max(0, new_h)

        self.size_bar.height = new_h
        self.size_bar.top = self.size_bar_bg.bottom - new_h

    def add_enemy(self, nx,ny):
        x = self.area.left + nx * self.area.width
        y = self.area.top + ny * self.area.height

        self.enemies.append(
            Enemy(
                self.area.width,
                'enemyship1.png',
                settings.ENEMY_MAX_HEALTH,
                settings.ENEMY_BASE_DAMAGE,
                settings.ENEMY_SPEED,
                x,y))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                pygame.mouse.set_visible(self.paused)
            if event.type == settings.PLAYER_DEATH:
                return "over"
        if self.paused:
            if self.cont_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                pygame.mouse.set_visible(False)
                self.paused = False
            if self.quit_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                return "QUIT"
        if not self.enemies:
            if self.num == 1:
                return "level2"
            if self.num == 2:
                return "level3"
            if self.num == 3:
                return "over"
        return f"level{self.num}"

    def update(self, events):
        if self.paused:
            return

        if not self.started:
            if pygame.time.get_ticks() - self.start_time > 2000:
                self.started = True

        #remove dead enemies
        self.enemies = [e for e in self.enemies if e.alive]

        for en in self.enemies:
            en.move( self.area)

        for event in events:
            # Resizing player with mousewheel
            if event.type == pygame.MOUSEWHEEL:
                self.p.resize(event.y)
                self.size_bar_resize()

            # Player shooting with left mouse click or space
            if ((event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)):
                if self.p.shoot():
                    self.projectiles.append(
                        Projectile(
                            self.p.x + self.p.shipsize / 2,
                            self.p.y, self.p.shipsize / 2,
                            settings.PROJECTILE_SPEED,
                            self.p.damage,
                            "player")
                    )
            # Enemy shooting automatically
            if event.type == settings.ENEMY_SHOOT:
                for en in self.enemies:
                    if en.shoot():
                        self.projectiles.append(
                            Projectile(
                                en.x + en.shipsize / 2,
                                en.y + en.shipsize,
                                en.shipsize / 2,
                                settings.PROJECTILE_SPEED,
                                en.damage,
                                en))

        for proj in self.projectiles:
            proj.move()
            # Check projectile for collision with enemies
            # if hit then add 5 points to score, print message with damage info,
            # remove projectile and damage the enemy
            if proj.shooter == "player":
                for en in self.enemies:
                    if proj.hitbox.colliderect(en.hitbox):
                        if not en.dying:
                            settings.score += 5
                            en.hit(proj.damage)
                        if proj in self.projectiles:
                            self.projectiles.remove(proj)
                        break

            else:
                # Check projectile for collision with player
                # if hit damage the player, remove projectile and print damage
                # info
                if proj.hitbox.colliderect(self.p.hitbox):
                    self.p.hit(proj.damage)
                    proj.shooter.promotion()
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    self.health_bar.width = self.health_bar_bg.width * (self.p.health / self.p.max_health)

                # Remove projectile if it goes off-screen
                if proj in self.projectiles and (
                        proj.y < 0 or proj.y > self.area.height):
                    self.projectiles.remove(proj)

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
            self.p.move(self.area, keys)

    def draw(self, screen):
        if self.paused:
            screen.blit(
                self.cont_text,
                (self.cont_btn.centerx - self.cont_text.get_width() // 2,
                 self.cont_btn.centery - self.cont_text.get_height() // 2)
            )
            screen.blit(
                self.quit_text,
                (self.quit_btn.centerx - self.quit_text.get_width() // 2,
                 self.quit_btn.centery - self.quit_text.get_height() // 2)
            )
            return

        screen.fill((50, 50, 50))
        pygame.draw.rect(screen, (255, 0, 0), self.health_bar_bg)
        pygame.draw.rect(screen, (0, 255, 0), self.health_bar)
        pygame.draw.rect(screen, (150, 150, 255), self.size_bar_bg)
        pygame.draw.rect(screen, (235, 180, 52), self.size_bar)
        screen.blit(self.ship_panels.left_panel, (0, 0))
        screen.blit(self.ship_panels.area_panel, (self.area.left, 0))
        screen.blit(self.ship_panels.right_panel, (self.area.left + self.area.width, 0))
        if not self.started:
            screen.blit(
                self.level_text,
                (screen.get_width() / 2 - self.level_text.get_width() / 2,
                 screen.get_height() / 2 - self.level_text.get_height() / 2))

        screen.blit(self.p.image, (self.p.x, self.p.y))
        for en in self.enemies:
            screen.blit(en.image, (en.x, en.y))
        for proj in self.projectiles:
            proj.draw(screen)