# I AI'd this part becuase I suck at design

import pygame
import sys

WIDTH, HEIGHT = 800, 600

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
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
]

OPERATORS = {"/", "*", "-", "+", "="}


class CalcButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, label):
        super().__init__()
        self.label = label
        self.rect = pygame.Rect(x, y, w, h)
        # thin ledge just under the button - this is what the player jumps to
        self.platform_rect = pygame.Rect(x, y + h, w, 6)
        self.color = ORANGE if label in OPERATORS else LIGHT_GRAY

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=6)
        pygame.draw.rect(screen, BLACK, self.rect, width=2, border_radius=6)
        pygame.draw.rect(screen, PLATFORM_COLOR, self.platform_rect)

        text = font.render(self.label, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


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
            buttons.append(CalcButton(x, y, btn_w, btn_h, label))

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
        draw_calculator(screen, buttons, font)
        pygame.display.flip()


if __name__ == "__main__":
    main()
