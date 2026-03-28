# pylint: disable=import-error, no-member
"""
Module for managing game state and global game settings.

Contains global variables for game settings, state tracking,
and lists of game objects (projectiles, enemies).
"""
import pygame
import player
import enemy
import projectile

pygame.init()

# Settings:
# general
FPS = 60
# enemy shooting cooldown
ENEMY_SHOOT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_SHOOT, 800)
# player
PLAYER_MAX_HEALTH = 100
PLAYER_SPEED = 4
PLAYER_BASE_DAMAGE = 53 # with 53 smallest size kills in 6 shots, biggest kills in 2 shots
PLAYER_DEATH = pygame.USEREVENT + 2
# enemy
ENEMY_MAX_HEALTH = 100
ENEMY_SPEED = 3.5
ENEMY_BASE_DAMAGE = 30
# boss
BOSS_MAX_HEALTH = 200
BOSS_SPEED = 5
BOSS_BASE_DAMAGE = 60
CHANCE_OF_DIRECTION_CHANGE = 0.01   # 0.01 = 1% chance
# projectile
PROJECTILE_SPEED = 6
# score to progress
LEVEL1_TARGET_SCORE = 100
LEVEL2_TARGET_SCORE = 500
LEVEL3_TARGET_SCORE = 800
# End of settings

font = pygame.font.SysFont('Futura', 20)
game_over_font = pygame.font.SysFont('Rocket', 100)
menu_font = pygame.font.SysFont('Futura', 90)
level_font = pygame.font.SysFont('Helvetica', 60)

"""
Initializes the game, creates player and starts the game loop.
"""
#fonts

score = 0
running = True
in_menu = True

class MainScreen:
    def __init__(self, area):
        self.area = area
        self.start_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height // 3 - 80, 200, 100)

        self.start_text = menu_font.render("Start", True, (255, 255, 255))

        self.howto_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height // 2 - 30, 200, 100)
        self.howto_text = menu_font.render("How To Play" , True, (255, 255, 255))

        self.quit_btn = pygame.Rect(
            (self.area.left + self.area.width // 2 - 100,
             self.area.height - self.area.height // 3 + 30, 200, 100))
        self.quit_text = menu_font.render("Quit", True, (255, 255, 255))

    def handle_events(self, events):
        if self.start_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return "level1"

        #TODO implement howto button

        if self.quit_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return "QUIT"
        return "main_menu"

    def update(self, events):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(
            self.start_text,
            (self.start_btn.centerx - self.start_text.get_width() // 2,
            self.start_btn.centery - self.start_text.get_height() // 2)
        )
        screen.blit(
            self.howto_text,
            (self.howto_btn.centerx - self.howto_text.get_width() // 2,
             self.howto_btn.centery - self.howto_text.get_height() // 2)
        )
        screen.blit(
            self.quit_text,
            (self.quit_btn.centerx - self.quit_text.get_width() // 2,
             self.quit_btn.centery - self.quit_text.get_height() // 2)
        )

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
        self.p = player.Player(
            'startership.png',
            PLAYER_MAX_HEALTH,
            PLAYER_BASE_DAMAGE,
            PLAYER_SPEED,
            self.area.left + self.area.width // 2 - 16,
            self.area.height - self.area.height // 4)
        #pause menu buttons
        self.cont_btn = pygame.Rect(
                self.area.left + self.area.width // 2 - 100,
                self.area.height // 3 - 50, 200, 100)
        self.cont_text = menu_font.render("Continue", True, (255, 255, 255))
        self.quit_btn = pygame.Rect(
            (self.area.left + self.area.width // 2 - 100,
             self.area.height - self.area.height // 3, 200, 100))
        self.quit_text = menu_font.render("Quit", True, (255, 255, 255))
        # level start text
        self.level_text = level_font.render(
            f"LEVEL {self.num}", True, (255, 10, 10))
        pygame.mouse.set_visible(False)
    def add_enemy(self, nx,ny):
        x = self.area.left + nx * self.area.width
        y = self.area.top + ny * self.area.height

        self.enemies.append(
            enemy.Enemy(
                'enemyship1.png',
                ENEMY_MAX_HEALTH,
                ENEMY_BASE_DAMAGE,
                ENEMY_SPEED,
                x,y))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                pygame.mouse.set_visible(self.paused)
            if event.type == PLAYER_DEATH:
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
            # Player shooting with left mouse click or space
            if ((event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE)):
                if self.p.shoot():
                    self.projectiles.append(
                        projectile.Projectile(
                            self.p.x + self.p.shipsize / 2,
                            self.p.y, self.p.shipsize / 2,
                            PROJECTILE_SPEED,
                            self.p.damage,
                            "player")
                    )
            # Enemy shooting automatically
            if event.type == ENEMY_SHOOT:
                for en in self.enemies:
                    if en.shoot():
                        self.projectiles.append(
                            projectile.Projectile(
                                en.x + en.shipsize / 2,
                                en.y + en.shipsize,
                                en.shipsize / 2,
                                PROJECTILE_SPEED,
                                en.damage,
                                en))

        for proj in self.projectiles:
            proj.move()
            # Check projectile for collision with enemies
            # if hit then add 5 points to score, print message with damage info,
            # remove projectile and damage the enemy
            global score
            if proj.shooter == "player":
                for en in self.enemies:
                    if proj.hitbox.colliderect(en.hitbox):
                        if not en.dying:
                            print("Player hit an enemy with: ",proj.damage," damage!")
                            score += 5
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
                    print(
                        "Enemy hit the player with: ",
                        proj.damage,
                        " damage!")
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)

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


class GameOverScreen:
    def __init__(self, area):
        self.area = area
        self.game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        self.score_text = menu_font.render(f"Score: {score}", True, (255, 255, 255))

        self.menu_btn = pygame.Rect(
            self.area.left + self.area.width // 2 - 100,
            self.area.height // 2 + 10, 200, 100)
        self.menu_text = menu_font.render("Main Menu", True, (255, 255, 255))

        self.quit_btn = pygame.Rect(
            (self.area.left + self.area.width // 2 - 100,
             self.area.height - self.area.height // 4 , 200, 100))
        self.quit_text = menu_font.render("Quit", True, (255, 255, 255))
        pygame.mouse.set_visible(True)

    def handle_events(self, events):
        if self.menu_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return "main_menu"

        if self.quit_btn.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return "QUIT"
        return "over"

    def update(self, events):
        pass

    def draw(self, screen):
        screen.fill((50, 50, 50))
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, self.area.left, screen.get_height()))
        pygame.draw.rect(screen, (20, 20, 20), self.area)
        pygame.draw.rect(screen, (50, 50, 50),(self.area.left + self.area.width, 0, screen.get_width(), screen.get_height()))
        screen.blit(
            self.game_over_text,
            (self.quit_btn.centerx - self.game_over_text.get_width() // 2,
             screen.get_height() // 5 - self.game_over_text.get_height() // 2 - 20)
        )
        screen.blit(
            self.score_text,
            (self.quit_btn.centerx - self.score_text.get_width() // 2,
             screen.get_height() // 4 + self.game_over_text.get_height() // 2 + 40)
        )
        screen.blit(
            self.menu_text,
            (self.menu_btn.centerx - self.menu_text.get_width() // 2,
             self.menu_btn.centery - self.menu_text.get_height() // 2)
        )
        screen.blit(
            self.quit_text,
            (self.quit_btn.centerx - self.quit_text.get_width() // 2,
             self.quit_btn.centery - self.quit_text.get_height() // 2)
        )


