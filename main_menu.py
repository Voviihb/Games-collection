import pygame
import sys
from scripts import load_image, Button
import flappy_bird
import minesweeper

FPS = 50

size = WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Сборник игр: главное меню")
clock = pygame.time.Clock()

sound_on = load_image("data/unmute.png", pygame)
sound_off = load_image("data/mute.png", pygame)
music_on = (sound_on, (30, 683))


def music():
    global music_on
    if sound_off in music_on:
        pygame.mixer.music.play()
        music_on = sound_on, (30, 683)
    else:
        pygame.mixer.music.stop()
        music_on = sound_off, (30, 682)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global music_on

    intro_text = ["СБОРНИК ИГР", "",
                  "Flappy bird,",
                  "Сапер,",
                  "Морской бой"]
    # Фон и постоянный текст
    background = pygame.transform.scale(load_image('data/menu_image.jpg', pygame), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    # Кнопки
    start_flappy_bird = Button(300, 70, screen, pygame)
    start_sapper = Button(170, 70, screen, pygame)
    quit_button = Button(200, 70, screen, pygame, active_clr=(255, 0, 0))
    music_button = Button(100, 100, screen, pygame)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.blit(background, (0, 0))
        start_flappy_bird.draw(300, 200, "Flappy bird", action=flappy_bird.flappy_bird, font_size=70)
        music_on_local = start_sapper.draw(700, 200, "Сапер", action=minesweeper.minesweeper, font_size=70, arg=music_on)
        if music_on_local:
            if music_on[1] != music_on_local[1]:
                music()

        quit_button.draw(500, 500, "Выход", action=terminate, font_size=70)
        music_button.draw(10, 658, "", action=music, font_size=70)
        screen.blit(*music_on)
        pygame.display.flip()
        clock.tick(60)
        clock.tick(FPS)


if __name__ == '__main__':

    pygame.init()

    pygame.mixer.music.load('data/8bit-background_main.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    start_screen()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
