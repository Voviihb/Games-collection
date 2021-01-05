import pygame
import sys
from scripts import load_image, Button, print_text, to_main_menu_button, pause_button_func, music, play_again_button
import random
import time

clock = pygame.time.Clock()

colour_list = ["black", "red", "green", "blue"]


def pause_logo(IF_PLAYING, play_button, pause_button):
    if IF_PLAYING:
        return play_button, (135, 5)
    else:
        return pause_button, (135, 5)


def draw_floor(floor_pos, screen, base, pause=False):
    if not pause:
        floor_pos -= 6/FPS*60
    screen.blit(base, (floor_pos, 705))
    screen.blit(base, (floor_pos + 1024, 705))
    if floor_pos <= -1024:
        floor_pos = 0
    return floor_pos


counter = 0
FPS = 30
WIDTH, HEIGHT = 1024, 768
IF_PLAYING = True
bird_sprite = pygame.sprite.Group()
floor_sprite = pygame.sprite.Group()
pipe_sprites = pygame.sprite.Group()

sound_on = load_image("data/unmute.png", pygame)
sound_off = load_image("data/mute.png", pygame)
pipe_up = load_image('data/flappy_bird/pipe-green_up.png', pygame)
pipe_down = load_image('data/flappy_bird/pipe-green_down.png', pygame)


class Pipe(pygame.sprite.Sprite):

    def __init__(self, radius=30, x=1000, y=300, place="bottom"):
        super().__init__(pipe_sprites)
        self.gened_next = False
        self.place = place
        if place == "bottom":
            self.image = pipe_down
            self.rect = pipe_down.get_rect()
            self.rect.x = x
            self.rect.y = HEIGHT - y
        if place == "top":
            self.image = pipe_up
            self.rect = pipe_up.get_rect()
            self.rect.x = x
            self.rect.y = HEIGHT - y - 200 - 626

    def update(self, arg=None):
        self.rect = self.rect.move(-6/FPS*60, 0)
        global counter
        if self.rect[0] < 0 or arg == "kill":
            self.kill()
        if self.rect[0] == 100 and self.place == "top":
            counter += 1

        elif self.rect[0] == 400 and self.place == "top":
            y = random.randint(100, 300)
            Pipe(y=y, place="bottom")
            Pipe(y=y, place="top")


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
        self.x = x
        self.y = y
        self.last_jump_time = time.time()
        self.jumped = False
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vy = 3/FPS*60

    def update(self, *args):
        if IF_PLAYING:
            self.rect = self.rect.move(0, self.vy)
            self.y += self.vy
            if self.jumped:
                if time.time() - self.last_jump_time > 1:
                    self.y -= 50
                    self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                                pygame.SRCALPHA, 32)
                    pygame.draw.circle(self.image, pygame.Color("red"),
                                       (self.radius, self.radius), self.radius)
                    self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
                    self.jumped = False
                    self.last_jump_time = time.time()

        if args:
            if "kill" in args:
                self.kill()
            if IF_PLAYING:
                self.y -= 50
                self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                            pygame.SRCALPHA, 32)
                pygame.draw.circle(self.image, pygame.Color("blue"),
                                   (self.radius, self.radius), self.radius)
                self.rect = pygame.Rect(self.x, self.y, 2 * self.radius, 2 * self.radius)
                self.rect = self.rect.move(0, -50)
                self.jumped = True

        if pygame.sprite.spritecollideany(self, floor_sprite) or pygame.sprite.spritecollideany(self, pipe_sprites):
            print("Game over")
            sys.exit()


def flappy_bird(music_on_imported):
    global bird_sprite, floor_sprite, pipe_sprites, IF_PLAYING, counter

    btns_top_coords = (0, 260), (0, 130)
    btns_floor_coords = [(0, 120), (650, 768)]

    close_button = load_image("data/close_button.png", pygame)
    pause_button = load_image("data/pause_button.png", pygame)
    play_button = load_image("data/play_button.png", pygame)
    restart_button = load_image("data/restart_button.png", pygame)

    music_on = sound_on, (30, 683)
    if music_on_imported[1] != music_on[1]:
        music_on = music(music_on, pygame, sound_on, sound_off)

    bird_sprite = pygame.sprite.Group()
    floor_sprite = pygame.sprite.Group()
    pipe_sprites = pygame.sprite.Group()

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

    to_main_menu_local = to_main_menu_button(screen, pygame)
    pause_local = pause_button_func(screen, pygame)
    music_button = Button(100, 100, screen, pygame)
    play_again_btn = play_again_button(screen, pygame)

    counter = 0

    y = random.randint(100, 300)
    Pipe(y=y, place="bottom")
    Pipe(y=y, place="top")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not (btns_floor_coords[0][0] < event.pos[0] < btns_floor_coords[0][1] and btns_floor_coords[1][0] <
                        event.pos[1] < btns_floor_coords[1][1]) \
                        and not (
                        btns_top_coords[0][0] < event.pos[0] < btns_top_coords[0][1] and btns_top_coords[1][0] <
                        event.pos[1] < btns_top_coords[1][1]):
                    bird_sprite.update(event)

        pygame.display.update()
        screen.blit(background, (0, 0))
        bird_sprite.draw(screen)
        pipe_sprites.draw(screen)
        if to_main_menu_local.draw(10, 10, "", font_size=70, cmd="close"):
            bird_sprite.update("kill")
            return music_on

        if pause_local.draw(140, 10, "", font_size=70, cmd="pause"):
            IF_PLAYING = not IF_PLAYING

        if play_again_btn.draw(270, 10, "", font_size=70, cmd="again"):
            counter = 0
            pipe_sprites.update("kill")
            y = random.randint(100, 300)
            Pipe(y=y, place="bottom")
            Pipe(y=y, place="top")
            print("restarted")

        if IF_PLAYING:
            bird_sprite.update()
            pipe_sprites.update()
            floor_x_pos = draw_floor(floor_x_pos, screen, base)  # перемещение пола
        else:
            floor_x_pos = draw_floor(floor_x_pos, screen, base, pause=True)

        if counter < 0:
            print_text("0", 450, 50, screen=screen, pygame=pygame, font_size=100)
        else:
            print_text(str(counter), 450, 50, screen=screen, pygame=pygame, font_size=100)

        a = music_button.draw(10, 658, "", action=music, font_size=70, args=(music_on, pygame, sound_on, sound_off))
        if a:
            music_on = a

        screen.blit(close_button, (20, 20))
        screen.blit(restart_button, (268, 10))
        screen.blit(*music_on)

        screen.blit(*pause_logo(IF_PLAYING, play_button, pause_button))

        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    flappy_bird((sound_on, (30, 683)))
