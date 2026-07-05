import sys
import pygame
import random
import math
from asteval import Interpreter

import pygame
import sys

WIDTH, HEIGHT = 800,600
PLAYER_SPEED = 3
GRAVITY = 0.5 # see technically this is the player's weight
JUMP_FORCE = -9

WHITE = (255, 255, 255)
BLUE = (50, 120, 200)
GREEN = (60, 180, 60)
RED = (200, 50, 50)

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
DARK_GRAY = (60, 60, 65)
LIGHT_GRAY = (210, 210, 215)
SCREEN_GREEN = (170, 200, 160)
ORANGE = (230, 150, 60)
PLATFORM_COLOR = (220, 60, 60)

# calculator body panel
CALC_X, CALC_Y = 150, 40
CALC_W, CALC_H = 500, 520

DISPLAY_H = 90
PADDING = 16

ROWS = [
    ["%", "√", "CE", "C"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
]

OPERATORS = {"/", "*", "-", "+", "="}

calc = Interpreter()

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

TIMER_START_FRAMES = 600
TIMER_FLASH_FRAMES = int(0.3 * FPS)
TIMER_BOX_W, TIMER_BOX_H = 150, 56
TIMER_BOX_MARGIN = 16

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
            global state_curr, state_prev, operator, display_text, operator_pressed
            if self.label.isnumeric() or self.label == '.':
                if operator_pressed:
                    state_curr = self.label
                    if self.label == '.':
                        state_curr = '0.'
                else:
                    if '.' not in state_curr or self.label != '.':
                        print(state_curr, self.label)
                        if state_curr == '0' and self.label != '.':
                            state_curr = self.label
                        else:
                            state_curr += self.label
                    # state_curr = f"{float(state_curr):g}"
                    if self.label == '.' and '.' not in state_curr:
                        state_curr += '.' 
                operator_pressed = False
            elif self.label == '√':
                state_curr = str(math.sqrt(float(state_curr)))
                operator_pressed = False
            elif self.label == '%':
                state_curr = str(float(state_curr) / 100)
                operator_pressed = False
            elif self.label == 'CE':
                state_curr = state_prev
                operator_pressed = True
            elif self.label == 'C':
                state_curr = '0'
                state_prev = '0'
                operator = ''
                operator_pressed = False
            elif self.label in ['/', '*', '-', '+']:
                if operator != '':
                    if operator_pressed:
                        operator = self.label
                        return
                    state_prev = f"{calc(state_prev + operator + state_curr):g}"
                    state_curr = state_prev
                else:
                    state_prev = state_curr
                    
                operator = self.label
                operator_pressed = True
            elif self.label == '=':
                if operator == '':
                    state_prev = state_curr
                else:
                    state_prev = f"{calc(state_prev + operator + state_curr):g}"
                    state_curr = state_prev
                    equal(state_prev)
                operator = ''
                operator_pressed = True
                
            display_text = state_curr if self.label != 'CE' else '0'
            print(state_prev, operator, state_curr, display_text, operator_pressed)

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


active_platforms = []

time_left = TIMER_START_FRAMES
timer_flash = 0  # frames remaining to show the flash color
timer_flash_color = None
game_over = False


def create_calculator_buttons():
    buttons = []
    grid_w = CALC_W - PADDING * 2
    grid_h = CALC_H - DISPLAY_H - PADDING * 3
    cols = len(ROWS[0])
    rows = len(ROWS)

    gap = 10
    btn_w = (grid_w - gap * (cols - 1)) / cols
    btn_h = (grid_h - gap * (rows - 1)) / rows

    grid_top = CALC_Y + PADDING * 2 + DISPLAY_H

    for row_i, row in enumerate(ROWS):
        for col_i, label in enumerate(row):
            x = CALC_X + PADDING + col_i * (btn_w + gap)
            y = grid_top + row_i * (btn_h + gap)
            button = CalcButton(x, y, btn_w, btn_h, label)
            button.platform_rect.image.fill(RED)
            buttons.append(button)

    return buttons


def get_platform_rects(buttons):
    """Rects for the thin ledges under each button, for use as jump platforms."""
    return [b.platform_rect for b in buttons]


def draw_calculator(screen, buttons, font, display_text=""):
    # calculator body
    pygame.draw.rect(screen, DARK_GRAY, (CALC_X, CALC_Y, CALC_W, CALC_H), border_radius=14)

    # display screen
    display_rect = pygame.Rect(CALC_X + PADDING, CALC_Y + PADDING, CALC_W - PADDING * 2, DISPLAY_H)
    pygame.draw.rect(screen, SCREEN_GREEN, display_rect, border_radius=4)
    pygame.draw.rect(screen, BLACK, display_rect, width=2, border_radius=4)

    if display_text:
        text = font.render(display_text, True, BLACK)
        text_rect = text.get_rect(bottomright=(display_rect.right - 10, display_rect.bottom - 10))
        screen.blit(text, text_rect)

    for button in buttons:
        button.draw(screen, font)


def draw_timer(screen, font):
    box_rect = pygame.Rect(WIDTH - TIMER_BOX_W - TIMER_BOX_MARGIN, TIMER_BOX_MARGIN, TIMER_BOX_W, TIMER_BOX_H)
    bg_color = timer_flash_color if timer_flash > 0 else DARK_GRAY
    pygame.draw.rect(screen, bg_color, box_rect, border_radius=8)
    pygame.draw.rect(screen, BLACK, box_rect, width=2, border_radius=8)

    text = font.render(str(max(0, time_left)), True, WHITE)
    text_rect = text.get_rect(center=box_rect.center)
    screen.blit(text, text_rect)


def equal(val):
    global time_left, timer_flash, timer_flash_color
    delta = float(val)
    time_left = max(0, int(time_left + delta))
    timer_flash = TIMER_FLASH_FRAMES
    timer_flash_color = GREEN if delta >= 0 else RED

grid_w = CALC_W - PADDING * 2
grid_h = CALC_H - DISPLAY_H - PADDING * 3
cols = len(ROWS[0])
rows = len(ROWS)

gap = 10
btn_w = (grid_w - gap * (cols - 1)) / cols
# btn_h = 

grid_top = CALC_Y + PADDING * 2 + DISPLAY_H

platform_list = []

for row_i in range(1, len(ROWS)+1):
    for j in range (4): # random 5 platforms per row
        x = random.random() * grid_w + PADDING + (btn_w + gap)
        y = grid_top + (row_i - random.random()+1) * ((grid_h - gap * (rows - 1)) / rows + gap)
            
        platform_list.append(Platform(x,y,40, 6))

platforms = pygame.sprite.Group(
    Platform(0, HEIGHT - 40, WIDTH, 40),   # temp ground

    *platform_list
)
# OK so simple calculators store two things: State A (previous total), operator, and State B (current total)/
# Pressing execute will execute the instruction


state_prev = '0'
operator = ''
state_curr = '0'
operator_pressed = False # operator JUST pressed

display_text = "0"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("calculator")
clock = pygame.time.Clock()
running = True



player = Player(100, 100)
active_buttons = create_calculator_buttons()

active_platforms = []

for button in active_buttons:
    active_platforms.append(button.platform_rect)

platforms = pygame.sprite.Group(*platforms, *active_platforms)
    
all_sprites = pygame.sprite.Group(player, *platforms)

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        player.update(platforms)
        platforms.update()

        if timer_flash > 0:
            timer_flash -= 1

        time_left -= 1
        if time_left <= 0:
            time_left = 0
            game_over = True

    screen.fill(WHITE)
    draw_calculator(screen,active_buttons, pygame.font.SysFont("courier", 28, bold=True), display_text=display_text)
    draw_timer(screen, pygame.font.SysFont("courier", 28, bold=True))
    all_sprites.draw(screen)

    if game_over:
        over_font = pygame.font.SysFont("courier", 64, bold=True)
        text = over_font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
pygame.quit()