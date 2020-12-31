import pygame, sys, os


def load_image(name, pygame, colorkey=None):
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
        if "png" not in fullname:
            image = image.convert_alpha()
    return image


def render_text(place, x=10, y=10, text="sample", scale=30, colour=(0, 255, 0)):
    f1 = pygame.font.Font(None, scale)
    text1 = f1.render(text, True, colour)
    place.blit(text1, (x, y))


def print_text(message, x, y, screen, pygame, font_size=30):
    font = pygame.font.Font(None, font_size)
    string_rendered = font.render(message, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = y
    intro_rect.x = x
    screen.blit(string_rendered, intro_rect)


class Button:
    def __init__(self, width, height, screen, pygame=None, inactive_clr=(13, 162, 58), active_clr=(23, 204, 58)):
        self.screen = screen
        self.pygame = pygame
        self.pygame.init()
        self.btn_sound = self.pygame.mixer.Sound('data/sound_btn_1.mp3')
        self.width = width
        self.height = height
        self.inactive_clr = inactive_clr
        self.active_clr = active_clr

    def draw(self, x, y, message, action=None, font_size=50, cmd=None):
        mouse = self.pygame.mouse.get_pos()
        click = self.pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            self.pygame.draw.rect(self.screen, self.active_clr, (x, y, self.width, self.height))

            if click[0] == 1:
                self.pygame.mixer.Sound.play(self.btn_sound)
                self.pygame.time.delay(50)
                if action:
                    action()
                if cmd:
                    return cmd
        else:
            self.pygame.draw.rect(self.screen, self.inactive_clr, (x, y, self.width, self.height))
        print_text(message, x + 10, y + 10, self.screen, self.pygame, font_size=font_size)


def to_main_menu_button(screen, pygame):
    return Button(120, 120, screen, pygame, active_clr=(255, 0, 0))


def pause_button_func(screen, pygame):
    return Button(120, 120, screen, pygame, active_clr=(255, 0, 0))
