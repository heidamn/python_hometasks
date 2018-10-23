import random
import time
def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid

def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()

def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    values1 = values
    values = []
    line = []
    for i in range(n):
        for j in range(n*i, n*(i+1)):
            line.append(values1[j])
        values.append(line)
        line = []
    return values

def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row = values[pos[0]]
    return row

def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = []
    for num in values:
        col.append(num[pos[1]])
    return col

def get_block(values, pos):
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

def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '.':
                empty_pos = (row, col)
                return empty_pos

def find_possible_values(grid, pos):
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    block = set(get_block(grid, pos))
    col = set(get_col(grid, pos))
    row = set(get_row(grid, pos))
    values = set('123456789')
    return values - block - col - row

def solve(grid):
    """
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    """
    Решение пазла, заданного в grid
        Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    """
    empty_pos = find_empty_positions(grid)  # находим пустую позицию
    if not empty_pos:  # если ее нет - возвращаем решенное судоку(причем возврат будет до начала рекурсии)
        return grid
    row, col = empty_pos  # для удобства находим ряд и столбец пустой ячейки
    if find_possible_values(grid, empty_pos):  # если есть возможные значения - уйти в рекурсию и дальнейшую подстановку
        for i in find_possible_values(grid, empty_pos):  # пока не найдем значение, для которого остальной пазл не сложится
            grid[row][col] = i  # добавляем значение к ячейке
            solution = solve(grid)  # решаем оставшийся пазл (рекурсия)
            if solution:  # если нашлось решение оставшихся ячеек, возвращаем его в начало рекурсии, если ни для одного значения решений не нашлось, далее будет возврщен None
                return solution
    grid[row][col] = '.'  # последняя ячейка так и не была найдена, стираем ее значение
    return None  # значения для ячейки нет, поэтому надо вернуться к прошлой ситуации

def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    for i in range(9):
        row = get_row(solution, (i, 0))
        for num in row:
            if row.count(num) > 1:
                return False
    for i in range(9):
        col = get_col(solution, (0, i))
        for num in col:
            if col.count(num) > 1:
                return False
    for i in range(9):
        block = get_block(solution, (i // 3 * 3, i % 3 * 3))
        for num in block:
            if block.count(num) > 1:
                return False
    return True

def generate_sudoku(N):
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
    #c    grid = solve([['.' for col in range(9)]for row in range(9)])
    if N > 81:
        numb = 0
    elif N < 0:
        numb = 81
    else:
        numb = 81 - N
    while numb != 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != '.':
            grid[row][col] = '.'
            numb -= 1
    return grid

if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        start = time.time()
        display(grid)
        solution = solve(grid)
        end = time.time()
        display(solution)
        print(f'{fname}: {end-start}')
