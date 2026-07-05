from init.constants import *
from init.libraries import *
from init.classes import *

import pygame
import sys
from setup import *



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

    player.update(platforms)

    screen.fill(WHITE)
    draw_calculator(screen,active_buttons, pygame.font.SysFont("courier", 28, bold=True))
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()