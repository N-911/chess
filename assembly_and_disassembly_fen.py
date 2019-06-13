"""
Условие задачи
Создать структуру для хранения позиции.
Написать функцию для парсинга FEN-позиции в эту структуру.
Написать функцию для формирования FEN-строки из этой структуры.
Дано: FEN-позиция, записанная с небольшими неточностями.
Надо: FEN-строка, созданная по данной позиции.
"""


input_f = "rnbqkbnr/pppppppp/8/8/8/17/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
figures = input_f.split()[0]
move = input_f.split()[1]
castling = input_f.split()[2]
halfway = input_f.split()[3]
w_move = input_f.split()[4]
b_move = input_f.split()[5]


def assemble_fen():
    k = ['2', '3', 'd', 'f', 'e', '1', 'f', '3', '5', 'd']
    for i in range(len(k)):
        if k[i].isdigit() and k[i + 1].isdigit():
            k[i] = int(k[i]) + int(k[i + 1])
            k[i + 1] = ' '

location_figures = figures.split('/')

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

print(figures)
print(move)
print(castling)
print(halfway)
print(w_move)
print(b_move)


