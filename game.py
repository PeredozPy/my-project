import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SLICE_DISPLAY_TIME = 100
ESC_HOLD_TIME = 2000
FPS = 60

class GameObject:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Hero(GameObject):
    def __init__(self, image_path, position):
        super().__init__(image_path, position)
        self.speed = 5
        self.jump_height = 10
        self.gravity = 1
        self.is_jumping = False
        self.jump_velocity = self.jump_height
        self.health = 80
        self.damage_min = 40
        self.damage_max = 75
        self.slice_active = False
        self.slice_image = pygame.image.load('untitleds/slice.png')
        self.slice_rect = None

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and not self.is_jumping:
            self.is_jumping = True
            self.jump_velocity = self.jump_height
        if keys[pygame.K_DOWN]:
            if random.random() < 0.8:
                pass
            else:
                self.health -= 65
        if keys[pygame.K_z] and not self.slice_active:
            self.slice_active = True
            self.slice_rect = self.slice_image.get_rect(midtop=self.rect.midright)
            pygame.time.set_timer(pygame.USEREVENT + 1, SLICE_DISPLAY_TIME)

    def update_jump(self):
        if self.is_jumping:
            self.rect.y -= self.jump_velocity
            self.jump_velocity -= self.gravity
            if self.jump_velocity < -self.jump_height:
                self.is_jumping = False
                self.jump_velocity = self.jump_height

    def draw_slice(self, screen):
        if self.slice_active:
            screen.blit(self.slice_image, self.slice_rect)

    def update_slice(self, event):
        if event.type == pygame.USEREVENT + 1:
            self.slice_active = False

class Enemy(GameObject):
    def __init__(self, image_path, position):
        super().__init__(image_path, position)
        self.health = 120
        self.damage = 65

    def move_towards(self, target):
        if target.rect.x < self.rect.x:
            self.rect.x -= 2
        elif target.rect.x > self.rect.x:
            self.rect.x += 2
        if target.rect.y < self.rect.y:
            self.rect.y -= 2
        elif target.rect.y > self.rect.y:
            self.rect.y += 2

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Soul Smasher")
        self.clock = pygame.time.Clock()
        self.background = GameObject('untitleds/bg.png', (0, 0))
        self.hero = Hero('untitleds/hero.png', (0, 300))
        self.enemies = [Enemy('untitleds/enemy.png', (500, 100))]
        self.esc_pressed_time = 0
        self.fullscreen = False

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.USEREVENT + 1:
                    self.hero.update_slice(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()

            keys = pygame.key.get_pressed()
            self.hero.move(keys)
            self.hero.update_jump()

            if keys[pygame.K_ESCAPE]:
                if self.esc_pressed_time == 0:
                    self.esc_pressed_time = current_time
                elif current_time - self.esc_pressed_time >= ESC_HOLD_TIME:
                    pygame.quit()
                    sys.exit()
            else:
                self.esc_pressed_time = 0

            self.screen.blit(self.background.image, self.background.rect)
            self.hero.draw(self.screen)
            self.hero.draw_slice(self.screen)

            for enemy in self.enemies:
                screen_width, screen_height = self.screen.get_size()
                if 0 <= enemy.rect.x <= screen_width and 0 <= enemy.rect.y <= screen_height:
                    enemy.move_towards(self.hero)
                enemy.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

if __name__ == "__main__":
    game = Game()
    game.run()