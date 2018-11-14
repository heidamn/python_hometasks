""" Лабораторная работа №3
    Игра Жизнь
    Шоломов Даниил, k3140
    ИТМО, 2018
    """

import random
from copy import deepcopy
import pygame
from pygame.locals import *


class GameOfLife:
    """класс визуализации и процесса игры"""

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)
        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_cell_list(self, celllist):
        """ Отображение списка клеток
        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        for rown, row in enumerate(celllist.clist):
            for coln, col in enumerate(row):
                if col.is_alive():
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (coln * self.cell_size, rown * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (coln * self.cell_size, rown * self.cell_size, self.cell_size, self.cell_size))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        celllist = CellList(self.cell_width, self.cell_height, randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(celllist)
            celllist.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:
    """Класс, описывающий отдельную клетку поля """

    def __init__(self, row, col, state=False):
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self):
        """ Проверка статуса клетки"""

        return self.state


class CellList:
    """ Класс игрового поля, состоящего из клеток"""

    def __init__(self, nrows, ncols, randomize=False):
        self.nrows = nrows
        self.ncols = ncols
        self.randomize = randomize
        if randomize:
            clist = [[Cell(rown, coln, state=random.randint(0, 1)) for coln in range(ncols)] for rown in range(nrows)]
        else:
            clist = [[Cell(rown, coln, state=False) for coln in range(ncols)] for rown in range(nrows)]
        self.clist = clist

    def get_neighbours(self, cell):
        """ Получение состояния соседних клеток """

        return [self.clist[rown + cell.row][coln + cell.col] for rown in range(-1, 2) for coln in range(-1, 2) if (coln or rown) and 0 <= cell.row + rown < self.nrows and 0 <= cell.col + coln < self.ncols]

    def update(self):
        """ Обновление игрового поля """
        new_clist = deepcopy(self.clist)
        for cell in self:
            neighbours = self.get_neighbours(cell)
            neighbours_num = 0
            for neighbour in neighbours:
                if neighbour.is_alive():
                    neighbours_num += 1
            if (neighbours_num == 2 and cell.is_alive()) or neighbours_num == 3:
                new_clist[cell.row][cell.col] = Cell(cell.row, cell.col, state=True)
            else:
                new_clist[cell.row][cell.col] = Cell(cell.row, cell.col, state=False)
        self.clist = new_clist
        return self

    @classmethod
    def from_file(cls, filename):
        """ Получение поля из файла """
        cells = open(filename).read()
        nrows = cells.count('\n')
        cells = [bool(int(c)) for c in cells if c in '01']
        ncols = len(cells) // nrows
        grid = CellList(nrows, ncols)
        count = 0
        for rown in range(nrows):
            for coln in range(ncols):
                grid.clist[rown][coln].state = cells[rown * ncols + coln]
                count += 1
        return grid

    def __iter__(self):
        self.row_count, self.col_count = 0, 0
        return self

    def __next__(self):
        if self.row_count == self.nrows:
            raise StopIteration
        cell = self.clist[self.row_count][self.col_count]
        self.col_count += 1
        if self.col_count == self.ncols:
            self.col_count = 0
            self.row_count += 1
        return cell

    def __str__(self):
        strclist = ''
        for cell in self:
            if cell.is_alive():
                strclist += '1 '
            else:
                strclist += '0 '
            if cell.col == self.ncols - 1:
                strclist += '\n'
        return strclist


if __name__ == '__main__':
    game = GameOfLife(800, 40, 20)
    game.run()
