import pygame
import sys, os
import time
FPS = 50

size = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Сборник игр: главное меню")
clock = pygame.time.Clock()


def print_text(message, x, y, font_size=30):
    font = pygame.font.Font(None, font_size)
    string_rendered = font.render(message, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = y
    intro_rect.x = x
    screen.blit(string_rendered, intro_rect)


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_clr = (13, 162, 58)
        self.active_clr = (23, 204, 58)

    def draw(self, x, y, message, action=None, font_size=50):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(screen, self.active_clr, (x, y, self.width, self.height))

            if click[0] == 1:
                # pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(50)
                if action:
                    action()
        else:
            pygame.draw.rect(screen, self.inactive_clr, (x, y, self.width, self.height))
        print_text(message=message, x=x + 10, y=y + 10, font_size=font_size)


def load_image(name, colorkey=None):
    fullname = name
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["СБОРНИК ИГР", "",
                  "Flappy bird,",
                  "Сапер,",
                  "Морской бой"]
    # Фон и постоянный текст
    fon = pygame.transform.scale(load_image('data/menu_image.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
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
    start_flappy_bird = Button(300, 70)
    start_flappy_sapper = Button(170, 70)
    quit_button = Button(200, 70)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        start_flappy_bird.draw(300, 200, "Flappy bird", font_size=70)
        start_flappy_sapper.draw(700, 200, "Сапер", font_size=70)
        quit_button.draw(500, 500, "Выход", action=terminate, font_size=70)
        pygame.display.flip()
        clock.tick(60)
        clock.tick(FPS)


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.flip()
    start_screen()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
