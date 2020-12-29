import pygame
from random import randrange
import sys
from scripts import Button


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
        if self.left <= pos[0] <= self.size_x and self.top <= pos[1] <= self.size_y:
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
    def __init__(self, width, height, mines_count):
        self.width = width
        self.height = height
        self.mines_count = mines_count
        self.board = [[-1] * width for _ in range(height)]
        for i in range(mines_count):
            x = randrange(self.width)
            y = randrange(self.height)
            if self.board[y][x] != 10:
                self.board[y][x] = 10
        # print(self.board)
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.size_x = self.width * self.cell_size + self.left
        self.size_y = self.height * self.cell_size + self.top

    def render(self, place):
        self.place = place
        cur_y = self.top
        for i in range(self.height):
            cur_x = self.left
            for j in range(self.width):
                if self.board[i][j] == 10:
                    pygame.draw.rect(place, (255, 0, 0), (cur_x, cur_y, self.cell_size, self.cell_size))
                elif self.board[i][j] in (0, 1, 2, 3, 4, 5, 6, 7, 8):
                    f1 = pygame.font.Font(None, 36)
                    text1 = f1.render(str(self.board[i][j]), True, (0, 255, 0))
                    place.blit(text1, (cur_x, cur_y))
                else:
                    pygame.draw.rect(place, (255, 255, 255), (cur_x, cur_y, self.cell_size, self.cell_size), 1)
                cur_x += self.cell_size
            cur_y += self.cell_size

    def is_mine(self, x, y):
        if self.board[y][x] == 10:
            return True
        return False

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.open_cell(cell)

    def open_cell(self, cell):
        try:
            x, y = cell[0], cell[1]
            counter = 0
            if self.board[y][x] == -1:
                if 1 <= x <= self.width - 2 and 1 <= y <= self.height - 2:
                    if self.is_mine(x - 1, y + 1):
                        counter += 1
                    if self.is_mine(x - 1, y):
                        counter += 1
                    if self.is_mine(x - 1, y - 1):
                        counter += 1
                    if self.is_mine(x, y + 1):
                        counter += 1
                    if self.is_mine(x, y - 1):
                        counter += 1
                    if self.is_mine(x + 1, y + 1):
                        counter += 1
                    if self.is_mine(x + 1, y):
                        counter += 1
                    if self.is_mine(x + 1, y - 1):
                        counter += 1

                elif x == 0 and 1 <= y <= self.height - 2:
                    if self.is_mine(x, y + 1):
                        counter += 1
                    if self.is_mine(x, y - 1):
                        counter += 1
                    if self.is_mine(x + 1, y + 1):
                        counter += 1
                    if self.is_mine(x + 1, y):
                        counter += 1
                    if self.is_mine(x + 1, y - 1):
                        counter += 1

                elif x == self.width - 1 and 1 <= y <= self.height - 2:
                    if self.is_mine(x - 1, y + 1):
                        counter += 1
                    if self.is_mine(x - 1, y):
                        counter += 1
                    if self.is_mine(x - 1, y - 1):
                        counter += 1
                    if self.is_mine(x, y + 1):
                        counter += 1
                    if self.is_mine(x, y - 1):
                        counter += 1
                elif y == 0 and 1 <= x <= self.width - 2:
                    if self.is_mine(x - 1, y):
                        counter += 1
                    if self.is_mine(x - 1, y + 1):
                        counter += 1
                    if self.is_mine(x, y + 1):
                        counter += 1
                    if self.is_mine(x + 1, y):
                        counter += 1
                    if self.is_mine(x + 1, y + 1):
                        counter += 1
                elif y == self.height - 1 and 1 <= x <= self.width - 2:
                    if self.is_mine(x - 1, y - 1):
                        counter += 1
                    if self.is_mine(x - 1, y):
                        counter += 1
                    if self.is_mine(x, y - 1):
                        counter += 1
                    if self.is_mine(x + 1, y - 1):
                        counter += 1
                    if self.is_mine(x + 1, y):
                        counter += 1
                elif x == 0 and y == 0:
                    if self.is_mine(x, y + 1):
                        counter += 1
                    if self.is_mine(x + 1, y + 1):
                        counter += 1
                    if self.is_mine(x + 1, y):
                        counter += 1
                elif x == 0 and y == self.height - 1:
                    if self.is_mine(x, y - 1):
                        counter += 1
                    if self.is_mine(x + 1, y - 1):
                        counter += 1
                    if self.is_mine(x + 1, y):
                        counter += 1
                elif x == self.width - 1 and y == 0:
                    if self.is_mine(x - 1, y):
                        counter += 1
                    if self.is_mine(x - 1, y + 1):
                        counter += 1
                    if self.is_mine(x, y + 1):
                        counter += 1
                elif x == self.width - 1 and self.height - 1:
                    if self.is_mine(x - 1, y - 1):
                        counter += 1
                    if self.is_mine(x - 1, y):
                        counter += 1
                    if self.is_mine(x, y - 1):
                        counter += 1
                self.board[y][x] = counter
        except:
            pass
        # coords = (self.cell_size * x + self.left, self.cell_size * y + self.top)
        # self.draw(coords, counter)

    # def draw(self, coords, counter):
    #     screen = self.place
    #     screen.fill((0, 0, 0))
    #     x, y = coords[0], coords[1]
    #     font = pygame.font.Font(None, 50)
    #     text = font.render(str(counter), True, (0, 255, 0))
    #     # text_x = x // 2 - text.get_width() // 2
    #     # text_y = y // 2 - text.get_height() // 2
    #     text_x = x
    #     text_y = y // 2
    #     screen.blit(text, (text_x, text_y))
    #     pygame.display.update()


def minesweeper():
    pygame.display.set_caption("Сборник игр: Сапер")
    size = width, height = 1024, 768
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    #pygame.display.flip()
    running = True
    flag = False
    r = 10
    v = 10  # пикселей в секунду
    clock = pygame.time.Clock()

    board = Minesweeper(10, 15, 10)
    board.set_view(10, 10, 35)
    to_main_menu = Button(300, 70, screen, pygame)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        if to_main_menu.draw(600, 100, "", font_size=70, cmd="close"):
            break
        board.render(screen)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    minesweeper()
    pygame.quit()
