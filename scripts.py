import sys, os

R, G, B = 0, 1, 2  # Constants to fast change color format


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


def render_text(place, pygame, x=10, y=10, text="sample", scale=30, colour=(0, 255, 0)):
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


def print_text_from_center(message, x, y, screen, pygame, font_size=30):
    font = pygame.font.Font(None, font_size)
    string_rendered = font.render(message, 1, pygame.Color('black'))
    TextW = string_rendered.get_width()
    TextH = string_rendered.get_height()
    TextRect = string_rendered.get_rect()
    TextRect.x = x - TextW // 2
    TextRect.top = y - TextH // 2
    screen.blit(string_rendered, TextRect)


class Button:
    def __init__(self, width, height, screen, pygame=None, inactive_clr=(13, 162, 58), active_clr=(23, 204, 58)):
        self.screen = screen
        self.pygame = pygame
        self.pygame.init()
        self.btn_sound = self.pygame.mixer.Sound('data/sound_btn_1.mp3')
        self.width = width
        self.height = height
        self.current_clr = list(inactive_clr)
        self.inactive_clr = inactive_clr
        self.active_clr = active_clr
        self.diff_clr = [(i - k) // 10 for i, k in zip(active_clr, inactive_clr)]

    def draw(self, x, y, message, action=None, font_size=50, cmd=None, arg=None, args=None):
        mouse = self.pygame.mouse.get_pos()
        click = self.pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            for i in range(len(self.current_clr)):
                if self.diff_clr[i] >= 0:
                    self.current_clr[i] = min(self.active_clr[i], self.current_clr[i] + self.diff_clr[i])
                else:
                    self.current_clr[i] = max(self.active_clr[i], self.current_clr[i] + self.diff_clr[i])
            if click[0] == 1:
                self.pygame.mixer.Sound.play(self.btn_sound)
                self.pygame.time.delay(50)
                if action:
                    if arg:
                        return action(arg)
                    elif args:
                        return action(*args)
                    else:
                        action()
                if cmd:
                    return cmd
        else:
            for i in range(len(self.current_clr)):
                if self.diff_clr[i] >= 0:
                    self.current_clr[i] = max(self.inactive_clr[i], self.current_clr[i] - self.diff_clr[i])
                else:
                    self.current_clr[i] = min(self.inactive_clr[i], self.current_clr[i] - self.diff_clr[i])

        rh = self.height // 3
        rw = self.width // 3
        MiddleRectSize = (self.width, self.height - rh * 2)
        topleft = (x + rh, y + rh)
        RectsSize = (self.width - rh * 2, self.height - rh * 2)
        self.pygame.draw.circle(self.screen, self.current_clr, topleft, rh, draw_top_left=True)
        self.pygame.draw.circle(self.screen, self.current_clr, (x + rh, y + self.height - rh), rh,
                                draw_bottom_left=True)
        self.pygame.draw.circle(self.screen, self.current_clr, (x + self.width - rh, y + rh), rh, draw_top_right=True)
        self.pygame.draw.circle(self.screen, self.current_clr, (x + self.width - rh, y + self.height - rh), rh,
                                draw_bottom_right=True)

        self.pygame.draw.rect(self.screen, self.current_clr, (x + rh, y) + RectsSize)  # Top rectangle
        self.pygame.draw.rect(self.screen, self.current_clr, (x, y + rh) + MiddleRectSize)  # Middle rectangle
        self.pygame.draw.rect(self.screen, self.current_clr, (x + rh, y + self.height - rh) + RectsSize)  # Bottom rect

        print_text_from_center(message, x + self.width // 2, y + self.height // 2, self.screen, self.pygame,
                               font_size=font_size)


def to_main_menu_button(screen, pygame):
    return Button(120, 120, screen, pygame, active_clr=(255, 0, 0))


def pause_button_func(screen, pygame):
    return Button(120, 120, screen, pygame, active_clr=(255, 0, 0))


def play_again_button(screen, pygame):
    return Button(120, 120, screen, pygame, active_clr=(255, 0, 0))


def music(music_on, pygame, sound_on, sound_off):
    if sound_off in music_on:
        pygame.mixer.music.play()
        return sound_on, (30, 683)
    else:
        pygame.mixer.music.stop()
        return sound_off, (30, 682)
