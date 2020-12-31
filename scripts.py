import pygame, sys, os


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


def render_text(place, x, y, text, scale, colour):
    f1 = pygame.font.Font(None, scale)
    text1 = f1.render(text, True, colour)
    place.blit(text1, (x, y))