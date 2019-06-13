"""
Дано расположение шахматных фигур на доске в FEN-нотации.
Вывести её в текстовом ASCII формате по образцу.
На диаграмме должно присутствовать:
    рамка вокруг позиции,
    буквы a-h снизу,
    цифры 1-8 слева,
    точки на пустых полях,
    фигуры на своих местах
Начальные данные: строка символов - позиция в FEN нотации
Вывод результата: 11 строчек по 21 символу на каждом.
  +-----------------+
8 | r n b q k b n r |
7 | p p p p p p p p |
6 | . . . . . . . . |
5 | . . . . . . . . |
4 | . . . . . . . . |
3 | . . . . . . . . |
2 | P P P P P P P P |
1 | R N B Q K B N R |
  +-----------------+
    a b c d e f g h
"""

input_f = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
# l = re.split('/| ', input_f)
first = input_f.split()[0]
location_figures = first.split('/')


def parse_board(location_figures):
    for y in range(len(location_figures)):
        row = location_figures[y]
        for i in range(8):
            if row[i].isdigit():
                row = row[:int(i)] + '.' * (int(row[i])) + row[(int(i)) + 1:]
        location_figures[y] = row
    return location_figures


location_figures = parse_board(location_figures)
matrix = [[None] * 8 for x in range(8)]
for i in range(8):
    for j in range(8):
        matrix[i][j] = location_figures[i][j]


def print_chess_board(matrix):
    board_matrix = [
        list('  +-----------------+'),
        list('8 |                 |'),
        list('7 |                 |'),
        list('6 |                 |'),
        list('5 |                 |'),
        list('4 |                 |'),
        list('3 |                 |'),
        list('2 |                 |'),
        list('1 |                 |'),
        list('  +-----------------+'),
        list('    a b c d e f g h  '), ]
    for i in range(8):
        f = 0
        for j in range(8):
            board_matrix[i + 1][j + 4 + f] = matrix[i][j]
            f += 1

    """plot board wirh figures"""
    for i in range(11):
        print(*board_matrix[i], sep='')
    print()
    return board_matrix


print_chess_board(matrix)
