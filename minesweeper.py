import pygame, time, sys, os
from random import randrange
from scripts import load_image, render_text, to_main_menu_button, Button, music, play_again_button

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

sound_on = load_image("data/unmute.png", pygame)
sound_off = load_image("data/mute.png", pygame)

tile_images = {
    '0': load_image('data/minesweeper/0.png', pygame),
    '1': load_image('data/minesweeper/1.png', pygame),
    '2': load_image('data/minesweeper/2.png', pygame),
    '3': load_image('data/minesweeper/3.png', pygame),
    '4': load_image('data/minesweeper/4.png', pygame),
    '5': load_image('data/minesweeper/5.png', pygame),
    '6': load_image('data/minesweeper/6.png', pygame),
    '7': load_image('data/minesweeper/7.png', pygame),
    '8': load_image('data/minesweeper/8.png', pygame),
    'bomb': load_image('data/minesweeper/bomb.png', pygame),
    'marked': load_image('data/minesweeper/flagged.png', pygame),
    'empty': load_image('data/minesweeper/facingDown.png', pygame)
}


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, tile_size):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.transform.scale(tile_images[tile_type], (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

    def update(self):
        self.kill()


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.size_x = self.width * self.cell_size + self.left
        self.size_y = self.height * self.cell_size + self.top

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.size_x = self.width * self.cell_size + self.left
        self.size_y = self.height * self.cell_size + self.top

    def render(self, place):
        cur_y = self.top
        for i in range(self.height):
            cur_x = self.left
            for j in range(self.width):
                pygame.draw.rect(place, (255, 255, 255), (cur_x, cur_y, self.cell_size, self.cell_size), 1)
                cur_x += self.cell_size
            cur_y += self.cell_size

    def get_cell(self, pos):
        if self.left < pos[0] < self.size_x and self.top < pos[1] < self.size_y:
            num_x = (pos[0] - self.left) // self.cell_size
            num_y = (pos[1] - self.top) // self.cell_size
            id = (num_x, num_y)
            return id
        else:
            return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        # self.on_click(cell)


class Minesweeper(Board):
    def __init__(self, mode=2, width=16, height=16, mines_count=40):
        self.lost = False
        self.not_win = True
        self.cheat_mode = False
        self.mode = mode
        if self.mode == 2:
            self.width = width
            self.height = height
            self.mines_count = mines_count
        elif self.mode == 1:
            self.width = 9
            self.height = 9
            self.mines_count = 10
            Minesweeper.set_view(self, 10, 10, 50)
        elif self.mode == 3:
            self.width = 9
            self.height = 9
            self.mines_count = 10
            self.cheat_mode = True
            Minesweeper.set_view(self, 10, 10, 50)
        elif self.mode == 4:
            self.width = width
            self.height = height
            self.mines_count = mines_count
            self.cheat_mode = True
            Minesweeper.set_view(self, 10, 10, 25)
        self.tagged_mines = 0
        self.board = [[-1] * width for _ in range(height)]
        # for i in range(mines_count):
        #     x = randrange(self.width)
        #     y = randrange(self.height)
        #     if self.board[y][x] != 10:
        #         self.board[y][x] = 10

        i = 0
        while i < self.mines_count:
            x = randrange(self.width)
            y = randrange(self.height)
            if self.board[y][x] != 10:
                self.board[y][x] = 10
                i += 1

        # print(self.board)
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.size_x = self.width * self.cell_size + self.left
        self.size_y = self.height * self.cell_size + self.top

    def render(self, place):
        all_sprites.update()
        self.place = place
        cur_y = self.top
        if not self.lost:
            e = int(time.time() - start_time)

            render_text(self.place, pygame, self.size_x + 30, 50, f"Mines left: {self.mines_count - self.tagged_mines}",
                        scale=30,
                        colour=(0, 255, 0))

            render_text(self.place, pygame, self.size_x + 30, 100,
                        f"Your time: {'{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60)}", scale=30,
                        colour=(0, 255, 0))
        else:
            render_text(self.place, pygame, self.size_x + 30, 50, f"Mines left: {self.result_left_mines}",
                        scale=30,
                        colour=(0, 255, 0))

            render_text(self.place, pygame, self.size_x + 30, 100,
                        f"Your time: {self.total_time}", scale=30,
                        colour=(0, 255, 0))

        for i in range(self.height):
            cur_x = self.left
            for j in range(self.width):
                if self.board[i][j] == 10 and self.lost or self.board[i][j] == 10 and self.cheat_mode:
                    Tile("empty", cur_x, cur_y, self.cell_size)
                    Tile("bomb", cur_x, cur_y, self.cell_size)
                    # pygame.draw.rect(place, (255, 0, 0), (cur_x, cur_y, self.cell_size - 1, self.cell_size - 1))
                elif self.lost and type(self.board[i][j]) == list and self.board[i][j][1] == 10:
                    Tile("marked", cur_x, cur_y, self.cell_size)
                    Tile("bomb", cur_x, cur_y, self.cell_size)
                elif self.board[i][j] in (0, 1, 2, 3, 4, 5, 6, 7, 8):
                    # f1 = pygame.font.Font(None, self.cell_size - 6)
                    # text1 = f1.render(str(self.board[i][j]), True, (0, 255, 0))
                    # place.blit(text1, (cur_x + self.cell_size // 3, cur_y + self.cell_size // 3))
                    Tile(str(self.board[i][j]), cur_x, cur_y, self.cell_size)
                elif type(self.board[i][j]) == list:
                    Tile("marked", cur_x, cur_y, self.cell_size)
                else:
                    Tile("empty", cur_x, cur_y, self.cell_size)
                    # pygame.draw.rect(place, (255, 255, 255), (cur_x, cur_y, self.cell_size, self.cell_size), 1)
                pygame.draw.rect(place, (0, 0, 0),
                                 (self.left, self.top, self.size_x - self.left, self.size_y - self.top), 3)
                cur_x += self.cell_size
            cur_y += self.cell_size

    def restart(self):
        self.__init__(self.mode)
        Minesweeper.set_view(self, 10, 10, 35)
        self.total_time = 0
        global start_time
        start_time = time.time()
        self.lost = False

    def is_mine(self, x, y):
        if self.board[y][x] == 10:
            return True
        return False

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.open_cell(cell)

    def mark_mine(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            x, y = cell[0], cell[1]
            if type(self.board[y][x]) != list and self.tagged_mines < self.mines_count:
                self.board[y][x] = ["marked", self.board[y][x]]
                self.tagged_mines += 1
                print("Marked", cell)
            elif type(self.board[y][x]) == list:
                self.board[y][x] = self.board[y][x][1]
                self.tagged_mines -= 1

    def open_cell(self, cell):
        x, y = cell[0], cell[1]
        counter = 0

        if self.board[y][x] == 10:
            self.lost = True
            e = int(time.time() - start_time)
            self.total_time = '{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60)
            self.result_left_mines = self.mines_count - self.tagged_mines
            print("YOU LOST")

        if self.board[y][x] == -1:
            for y_edge in range(-1, 2):
                for x_edge in range(-1, 2):
                    if x + x_edge < 0 or x + x_edge >= self.width or y + y_edge < 0 or y + y_edge >= self.height:
                        continue

                    if self.board[y + y_edge][x + x_edge] == 10:
                        counter += 1

            self.board[y][x] = counter

        if self.board[y][x] == 0:
            for y_edge in range(-1, 2):
                for x_edge in range(-1, 2):
                    if x + x_edge < 0 or x + x_edge >= self.width or y + y_edge < 0 or y + y_edge >= self.height:
                        continue

                    if self.board[y + y_edge][x + x_edge] == -1:
                        self.open_cell((x + x_edge, y + y_edge))

    def win(self):
        self.counter = 0
        if self.tagged_mines == self.mines_count:
            for i in range(self.height):
                for j in range(self.width):
                    if type(self.board[i][j]) == list and self.board[i][j][1] == 10:
                        self.counter += 1
            if self.counter != self.mines_count:
                print("Not all the mines have been marked")
                # print(self.board)
            else:
                print("You win!")
                e = int(time.time() - start_time)
                self.total_time = '{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60)
                self.result_left_mines = self.mines_count - self.tagged_mines
                return True
        return False


def minesweeper(music_on_imported):
    music_on = sound_on, (30, 683)
    if music_on_imported[1] != music_on[1]:
        music_on = music(music_on, pygame, sound_on, sound_off)
    screen = pygame.display.set_mode((1024, 768))
    FPS = 60
    pygame.display.set_caption("Сборник игр: Сапер")
    # start_screen()
    screen.fill((0, 0, 0))
    pygame.display.flip()
    start_screen(screen, FPS)
    close_button = load_image("data/close_button.png", pygame)
    restart_button = load_image("data/restart_button.png", pygame)
    music_button = Button(100, 100, screen, pygame)
    to_main_menu_local = to_main_menu_button(screen, pygame)
    play_again_but = play_again_button(screen, pygame)
    global start_time
    start_time = time.time()
    board = Minesweeper(g_mode)
    board.set_view(10, 10, 35)
    running = True
    while running:
        # all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not board.lost:
                    if event.button == 1:
                        board.get_click(event.pos)
                    elif event.button == 2:
                        print("middle mouse button")
                    elif event.button == 3:
                        board.mark_mine(event.pos)
                        if board.win():
                            board.lost = True

        screen.fill((187, 187, 187))
        # all_sprites.update()
        all_sprites.draw(screen)
        player_group.draw(screen)
        board.render(screen)

        if to_main_menu_local.draw(890, 640, "", font_size=70, cmd="close"):
            return music_on

        if play_again_but.draw(700, 640, "", font_size=70, cmd="again"):
            board.restart()

        screen.blit(close_button, (900, 650))
        screen.blit(restart_button, (700, 640))
        a = music_button.draw(10, 658, "", action=music, font_size=70, args=(music_on, pygame, sound_on, sound_off))
        if a:
            music_on = a
        screen.blit(*music_on)

        pygame.display.flip()
        if board.lost:
            pass


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen, FPS):
    intro_text = ["Правила игры",
                  "Число в ячейке показывает, сколько мин скрыто вокруг данной ячейки. ",
                  "Это число поможет понять вам, где находятся безопасные ячейки, а где находятся бомбы.",
                  "Если рядом с открытой ячейкой есть пустая ячейка, то она откроется автоматически.",
                  "Если вы открыли ячейку с миной, то игра проиграна..",
                  "Что бы пометить ячейку, в которой находится бомба, нажмите её правой кнопкой мыши.",
                  "После того, как вы отметите все мины, можно навести курсор на открытую ячейку и ",
                  "нажать правую и левую кнопку мыши одновременно. ",
                  "Тогда откроются все свободные ячейки вокруг неё",
                  "Если в ячейке указано число, оно показывает, ",
                  "сколько мин скрыто в восьми ячейках вокруг данной. ",
                  "Это число помогает понять, где находятся безопасные ячейки.",
                  "Игра продолжается до тех пор, пока вы не откроете все не заминированные ячейки.",
                  " ",
                  "Вам доступно 4 режима игры:",
                  "1. Простой. Поле 9x9, 10 мин",
                  "2. Средний. Поле 16x16, 40 мин",
                  "3. Простой с просмотром мин. Поле 9x9, 10 мин",
                  "4. Средний с просмотром мин. Поле 16x16, 40 мин",
                  " ",
                  "Для выбора нажмите соответствующую цифру на клавиатуре"]

    fullname = os.path.join('data/minesweeper', 'fon.jpg')
    fon = pygame.transform.scale(load_image(fullname, pygame), (1024, 768))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            keys = pygame.key.get_pressed()
            if keys:
                global g_mode
                if keys[pygame.K_1]:
                    g_mode = 1
                    return
                if keys[pygame.K_2]:
                    g_mode = 2
                    return
                if keys[pygame.K_3]:
                    g_mode = 3
                    return
                if keys[pygame.K_4]:
                    g_mode = 4
                    return
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Сапер beta 0.2')
    size = width, height = 800, 600
    minesweeper((sound_on, (30, 683)))
