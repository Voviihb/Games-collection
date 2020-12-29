import pygame
import sys
from scripts import load_image


def draw_floor(floor_pos):
    floor_pos -= 2
    screen.blit(base, (floor_pos, 705))
    screen.blit(base, (floor_pos + 1024, 705))
    if floor_pos <= -1024:
        floor_pos = 0
    return floor_pos


clock = pygame.time.Clock()
FPS = 60

if __name__ == '__main__':
    pygame.init()

WIDTH, HEIGHT = 1024, 768

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сборник игр: Flappy bird")
background = pygame.transform.scale(load_image('data/flappy_bird/background.png'), (WIDTH, HEIGHT))
base = pygame.transform.scale(load_image('data/flappy_bird/base.png'), (1024, 70))
floor_x_pos = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    screen.blit(background, (0, 0))
    floor_x_pos = draw_floor(floor_x_pos)  # перемещение пола

    clock.tick(FPS)
