# I AI'd this part becuase I suck at design

import pygame
import sys

from init.constants import *
from init.libraries import *
from init.classes import *



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
