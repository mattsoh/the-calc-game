# I AI'd this part becuase I suck at design

import pygame
import sys

from init.constants import *
from init.libraries import *
from init.classes import *


active_platforms = []

time = 50


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
# platforms.

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("calculator setup preview")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("courier", 28, bold=True)

    buttons = create_calculator_buttons()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_calculator(screen, buttons, font, display_text='0')
        pygame.display.flip()


if __name__ == "__main__":
    main()
