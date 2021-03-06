""" Лабораторная работа №3
    Игра Жизнь с использованием классов
    Шоломов Даниил, k3140
    ИТМО, 2018
    """

import random
from copy import deepcopy
import pygame
from pygame.locals import *


class GameOfLife:
    """класс визуализации и процесса игры"""

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
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

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_cell_list(self, celllist) -> None:
        """ Отображение списка клеток
        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        for rown, row in enumerate(celllist.clist):
            for coln, col in enumerate(row):
                if col.is_alive():
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (rown * self.cell_size, coln * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (rown * self.cell_size, coln * self.cell_size, self.cell_size, self.cell_size))

    def run(self) -> None:
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
            self.draw_cell_list(celllist)
            self.draw_grid()
            celllist.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:
    """Класс, описывающий отдельную клетку поля """

    def __init__(self, row: int, col: int, state: bool = False) -> None:
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self) -> bool:
        """ Проверка статуса клетки"""

        return self.state


class CellList:
    """ Класс игрового поля, состоящего из клеток"""

    def __init__(self, nrows: int, ncols: int, randomize: bool = False) -> None:
        self.nrows = nrows
        self.ncols = ncols
        self.randomize = randomize
        if randomize:
            clist = [[Cell(rown, coln, state=bool(random.randint(0, 1))) for coln in range(ncols)] for rown in range(nrows)]
        else:
            clist = [[Cell(rown, coln, state=False) for coln in range(ncols)] for rown in range(nrows)]
        self.clist = clist

    def get_neighbours(self, cell: Cell) -> list:
        """ Получение состояния соседних клеток """

        return [self.clist[rown + cell.row][coln + cell.col] for rown in range(-1, 2) for coln in range(-1, 2) if (coln or rown) and 0 <= cell.row + rown < self.nrows and 0 <= cell.col + coln < self.ncols]

    def update(self) -> object:
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
    def from_file(cls, filename: str) -> object:
        """ Получение поля из файла """
        with open(filename, 'r') as cells_file:
            cells_str = cells_file.read()
            nrows = cells_str.count('\n')
            cells = [bool(int(c)) for c in cells_str if c in '01']
        ncols = len(cells) // nrows
        grid = CellList(nrows, ncols)
        count = 0
        for cell in grid:
            cell.state = cells[count]
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
    game = GameOfLife(800, 600, 20)
    game.run()
