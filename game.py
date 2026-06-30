import pygame
import sys

WIDTH, HEIGHT = 800,600
PLAYER_SPEED = 5
GRAVITY = 0.5 # see technically this is the player's weight
JUMP_FORCE = -12

WHITE = (255, 255, 255)
BLUE = (50, 120, 200)
GREEN = (60, 180, 60)
RED = (200, 50, 50)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("calculator")
clock = pygame.time.Clock()
running = True

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_SPEED
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = JUMP_FORCE

        self.vel_y += GRAVITY
        self.rect.x += self.vel_x
        self._collide_x(platforms)
        self.rect.y += self.vel_y
        self.on_ground = False
        self._collide_y(platforms)

        if self.rect.top > HEIGHT:
            self.rect.topleft = (100,100)
            self.vel_y = 0
    
    def _collide_x(self, platforms):
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                elif self.vel_x < 0:
                    self.rect.left = p.rect.right

    def _collide_y(self, platforms):
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom
                self.vel_y = 0
                
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        

platforms = pygame.sprite.Group(
    Platform(0, HEIGHT - 40, WIDTH, 40),   # temp ground
    Platform(200, 450, 150, 20),
    Platform(400, 350, 150, 20),
    Platform(150, 250, 150, 20),
    Platform(500, 200, 150, 20),
)

player = Player(100, 100)
all_sprites = pygame.sprite.Group(player, *platforms)

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.update(platforms)

    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()