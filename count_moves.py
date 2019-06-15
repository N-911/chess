"""
Условие задачи
Дана FEN-позиция и ход фигурой.
Нужно посчитать этот ход и передать право хода другой стороне.
ФИГУРЫ ПЕРЕМЕЩАТЬ НЕ НУЖНО

Дано:
   FEN-позиция
   ход фигурой
Надо:
   FEN-позиция после хода

"""


class Chess:

    def __init__(self, fen):
        self.fen_list = fen.split()
        self.figures = fen.split()[0]
        self.move = fen.split()[1]
        self.castling = fen.split()[2]
        self.halfway = fen.split()[3]
        self.w_move = fen.split()[4]
        self.b_move = fen.split()[5]
        # self.xod = fen.split()[6]

    def print_fen(self):
        return self.fen_list

    def parse_location_figures(self):
        """парсит положение фигур - возвращает list строк позиций"""
        location_figures = self.figures.split('/')
        for y in range(len(location_figures)):
            row = location_figures[y]
            for i in range(8):
                if row[i].isdigit():
                    row = row[:int(i)] + '.' * (int(row[i])) + row[(int(i)) + 1:]
            location_figures[y] = row
        return location_figures

    def matrix_figures(self):
        """созадает матризу 8 на расположения фигур"""
        matrix = [[None] * 8 for x in range(8)]
        location_figures = self.parse_location_figures()
        for i in range(8):
            for j in range(8):
                matrix[i][j] = location_figures[i][j]
        return matrix

    def matrix_figures_str_fen(self):
        """преобразует матрицу фен в строку """
        array_l = ''
        for row in self.matrix_figures():
            for i in row:
                array_l += ''.join(i)
            array_l += '/'
        array_l = array_l.replace('.', '1') + ' '
        df = 'rnbqkbnrp/RNBQKBNRP'
        array_n = []
        number = 0
        for i in range(len(array_l)):
            if array_l[i].isdigit() and array_l[i + 1].isdigit():
                number += int(array_l[i])

            elif array_l[i].isdigit() and array_l[i + 1] in df:
                number += int(array_l[i])
                array_n.append(str(number))
                number = 0
            elif array_l[i] in df and array_l[i + 1] in df:
                array_n.append(array_l[i])
            elif array_l[i] in df and array_l[i + 1].isdigit():
                array_n.append(array_l[i])
        return ''.join(array_n)

    def assemblage_fen(self):
        return ' '.join([self.matrix_figures_str_fen(), self.move,
                         self.castling, self.halfway, self.w_move, self.b_move])

    def move_f(self):
        if xod:
            if self.move == 'w':
                self.move = 'b'
            else:
                self.move = 'w'
        return self.move


if __name__ == "__main__":
    fen = input(str())
    xod = input(str())
    chess1 = Chess(fen)
    chess1_fen = chess1.parse_location_figures()
    chess1.matrix_figures()
    chess1.move_f()
    we = chess1.matrix_figures_str_fen()
    print(chess1.assemblage_fen())
