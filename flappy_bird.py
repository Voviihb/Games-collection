import pygame
import sys
from scripts import load_image, Button, print_text
import random

clock = pygame.time.Clock()


def draw_floor(floor_pos, screen, base):
    floor_pos -= 2
    screen.blit(base, (floor_pos, 705))
    screen.blit(base, (floor_pos + 1024, 705))
    if floor_pos <= -1024:
        floor_pos = 0
    return floor_pos


FPS = 60
WIDTH, HEIGHT = 1024, 768
IF_PLAYING = True
bird_sprite = pygame.sprite.Group()
floor_sprite = pygame.sprite.Group()
pipe_sprites = pygame.sprite.Group()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, radius=30, x=1000, y=300, place="bottom"):
        super().__init__(pipe_sprites)

        if place == "bottom":
            self.image = pygame.Surface([50, y])
            self.rect = pygame.Rect(x, HEIGHT - y, 50, y)
        if place == "top":
            self.image = pygame.Surface([50, HEIGHT - y - 200])
            self.rect = pygame.Rect(x, 0, 50, HEIGHT - y - 200)

    def update(self):
        self.rect = self.rect.move(-10, 0)
        if self.rect[0] < 0:
            self.kill()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(floor_sprite)
        if x1 == x2:  # вертикальная стенка
            self.add(floor_sprite)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(floor_sprite)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Bird(pygame.sprite.Sprite):
    def __init__(self, radius=30, x=100, y=400):
        super().__init__(bird_sprite)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vy = 2

    def update(self, *args):
        self.rect = self.rect.move(0, self.vy)
        if args:
            if args == "kill":
                self.kill()
            else:
                self.rect = self.rect.move(0, -30)
        if pygame.sprite.spritecollideany(self, floor_sprite) or pygame.sprite.spritecollideany(self, pipe_sprites):
            print("Game over")
            sys.exit()


def flappy_bird():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Сборник игр: Flappy bird")
    background = pygame.transform.scale(load_image('data/flappy_bird/background.png', pygame), (WIDTH, HEIGHT))
    base = pygame.transform.scale(load_image('data/flappy_bird/base.png', pygame), (1024, 70))
    floor_x_pos = 0
    Bird()
    Border(5, 5, WIDTH - 5, 5)
    Border(70, HEIGHT - 70, WIDTH - 70, HEIGHT - 70)
    Border(5, 5, 5, HEIGHT - 5)
    Border(WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5)

    to_main_menu = Button(300, 70, screen, pygame)
    pause = Button(70, 70, screen, pygame)
    SPAWNPIPE = pygame.USEREVENT
    counter = -1
    pygame.time.set_timer(SPAWNPIPE, 1200)
    global IF_PLAYING
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird_sprite.update(event)
            if event.type == SPAWNPIPE and IF_PLAYING:
                y = random.randint(100, 300)
                Pipe(y=y, place="bottom")
                Pipe(y=y, place="top")
                counter += 1

        pygame.display.update()
        screen.blit(background, (0, 0))

        if to_main_menu.draw(100, 100, "", font_size=70, cmd="close"):
            bird_sprite.update("kill")
            break
        if pause.draw(700, 100, "", font_size=70, cmd="pause"):
            IF_PLAYING = not IF_PLAYING

        bird_sprite.draw(screen)
        pipe_sprites.draw(screen)
        if IF_PLAYING:
            floor_x_pos = draw_floor(floor_x_pos, screen, base)  # перемещение пола
            bird_sprite.update()
            pipe_sprites.update()

        if counter < 0:
            print_text("0", 450, 50, screen=screen, pygame=pygame, font_size=100)
        else:
            print_text(str(counter), 450, 50, screen=screen, pygame=pygame, font_size=100)

        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    flappy_bird()
