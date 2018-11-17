"""
sudoku for ITMO 2018
"""
import random
import time
from typing import List, Tuple, Optional, Set


def read_sudoku(filename: str) -> Optional[List]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    gridread = group(digits, 9)
    return gridread


def display(values: List):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: List, leng: int) -> List:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [[values[el + col] for el in range(leng)] for col in range(0, leng**2, leng)]


def get_row(values: List, pos: Tuple) -> List:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return values[pos[0]]


def get_col(values: List, pos: Tuple) -> List:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = pos[1]
    return [lin[col] for lin in values]


def get_block(values: List, pos: Tuple) -> List:
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block = []
    for row in range(pos[0] // 3 * 3, (pos[0] // 3 + 1) * 3):
        for col in range(pos[1] // 3 * 3, (pos[1] // 3 + 1) * 3):
            block.append(values[row][col])
    return block


def find_empty_positions(gridfep: List) -> Optional[Tuple]:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for rown, row in enumerate(gridfep):
        for coln, col in enumerate(row):
            if col == '.':
                empty_pos = (rown, coln)
                return empty_pos
    return None


def find_possible_values(gridfpv: List, pos: Tuple) -> Set:
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    block = set(get_block(gridfpv, pos))
    col = set(get_col(gridfpv, pos))
    row = set(get_row(gridfpv, pos))
    values = set('123456789')
    return values - block - col - row


def solve(grids: List) -> Optional[List]:
    """
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    empty_pos = find_empty_positions(grids)
    if not empty_pos:
        return grids
    row, col = empty_pos
    for i in find_possible_values(grids, empty_pos):
        grids[row][col] = i
        solutions = solve(grids)
        if solutions:
            return solutions
    grids[row][col] = '.'
    return None


def check_solution(solutioncs: List) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    for i in range(9):
        row = get_row(solutioncs, (i, 0))
        for num in row:
            if row.count(num) > 1:
                return False
    for i in range(9):
        col = get_col(solutioncs, (0, i))
        for num in col:
            if col.count(num) > 1:
                return False
    for i in range(9):
        block = get_block(solutioncs, (i // 3 * 3, i % 3 * 3))
        for num in block:
            if block.count(num) > 1:
                return False
    return True


def generate_sudoku(amount: int) -> List:
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    gridgs = solve([['.' for col in range(9)]for row in range(9)])
    if amount > 81:
        numb = 0
    elif amount < 0:
        numb = 81
    else:
        numb = 81 - amount
    while numb != 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if gridgs[row][col] != '.':
            gridgs[row][col] = '.'
            numb -= 1
    return gridgs


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        start = time.time()
        display(grid)
        solution = solve(grid)
        end = time.time()
        display(solution)
        print(f'{fname}: {end-start}')
