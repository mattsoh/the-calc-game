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

        collide = False
        
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
            if not p.solid:
                continue
            if self.rect.colliderect(p.rect):
                p.on_stepped_on()
                if self.vel_x > 0:
                    self.rect.right = p.rect.left
                elif self.vel_x < 0:
                    self.rect.left = p.rect.right
            
    def _collide_y(self, platforms):
        for p in platforms:
            if not p.solid:
                continue
            if self.rect.colliderect(p.rect):
                p.on_stepped_on()
                if self.vel_y > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = p.rect.bottom
                self.vel_y = 0
                return True
                
class CalcButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, label):
        super().__init__()
        self.label = label
        self.rect = pygame.Rect(x, y, w, h)
        # thin ledge just under the button - this is what the player jumps to
        self.platform_rect = ActivePlatform(x+20, y + h, w-40, 6, label)
        self.color = ORANGE if label in OPERATORS else LIGHT_GRAY

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        pygame.draw.rect(screen, BLACK, self.rect, width=2, border_radius=6)
        screen.blit(self.platform_rect.image, self.platform_rect.rect)

        text = font.render(self.label, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
                
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.solid = True

    def on_stepped_on(self):
        pass

    def update(self):
        pass


SHAKE_SECONDS = 2
GONE_SECONDS = 5
FALL_SECONDS = 0.3
FPS = 60
SHAKE_MAGNITUDE = 3

class ActivePlatform(Platform):
    """Red platform ledge: shakes when touched, falls away, then respawns."""

    def __init__(self, x, y, w, h, label):
        super().__init__(x, y, w, h)
        self.image.fill(PLATFORM_COLOR)
        self.origin = (x, y)
        self.state = "idle"  # idle -> shaking -> falling -> gone -> idle
        self.timer = 0
        self.label = label

    def on_stepped_on(self):
        if self.state == "idle":
            self.state = "shaking"
            self.timer = int(SHAKE_SECONDS * FPS)
            # evaluate instruction
            # if self.label.is_numeric():
                

    def update(self):
        if self.state == "shaking":
            self.timer -= 1
            self.rect.x = self.origin[0] + random.randint(-SHAKE_MAGNITUDE, SHAKE_MAGNITUDE)
            if self.timer <= 0:
                self.state = "falling"
                self.timer = int(FALL_SECONDS * FPS)
                self.solid = False

        elif self.state == "falling":
            self.timer -= 1
            self.rect.x = self.origin[0]
            self.rect.y += 4
            fall_length = max(1, int(FALL_SECONDS * FPS))
            self.image.set_alpha(max(0, int(255 * self.timer / fall_length)))
            if self.timer <= 0:
                self.state = "gone"
                self.timer = int(GONE_SECONDS * FPS)
                self.image.set_alpha(0)

        elif self.state == "gone":
            self.timer -= 1
            if self.timer <= 0:
                self.state = "idle"
                self.solid = True
                self.rect.topleft = self.origin
                self.image.set_alpha(255)

