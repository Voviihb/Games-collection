import pygame
import sys
from scripts import load_image, Button

clock = pygame.time.Clock()


def draw_floor(floor_pos, screen, base):
    floor_pos -= 2
    screen.blit(base, (floor_pos, 705))
    screen.blit(base, (floor_pos + 1024, 705))
    if floor_pos <= -1024:
        floor_pos = 0
    return floor_pos


FPS = 60


# if __name__ == '__main__':
#    pygame.init()


def flappy_bird():
    WIDTH, HEIGHT = 1024, 768

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Сборник игр: Flappy bird")
    background = pygame.transform.scale(load_image('data/flappy_bird/background.png', pygame), (WIDTH, HEIGHT))
    base = pygame.transform.scale(load_image('data/flappy_bird/base.png', pygame), (1024, 70))
    floor_x_pos = 0

    to_maim_menu = Button(300, 70, screen, pygame)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        screen.blit(background, (0, 0))
        if to_maim_menu.draw(100, 100, "", font_size=70, cmd="close"):
            break
        floor_x_pos = draw_floor(floor_x_pos, screen, base)  # перемещение пола

        clock.tick(FPS)
