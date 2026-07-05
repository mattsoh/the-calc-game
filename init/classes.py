from init.constants import *
from init.libraries import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 15))
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
                
class CalcButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, label):
        super().__init__()
        self.label = label
        self.rect = pygame.Rect(x, y, w, h)
        # thin ledge just under the button - this is what the player jumps to
        self.platform_rect = Platform(x+20, y + h, w-40, 6)
        self.color = ORANGE if label in OPERATORS else LIGHT_GRAY

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        pygame.draw.rect(screen, BLACK, self.rect, width=2, border_radius=6)
        pygame.draw.rect(screen, PLATFORM_COLOR, self.platform_rect)

        text = font.render(self.label, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
                
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        
