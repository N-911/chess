"""
Условие задачи
Дана FEN-позиция и ход фигурой.
Нужно посчитать этот ход, передать право хода другой стороне,
а также увеличить или сбросить счётчик полуходов для правила 50 ходов.
Счётчик сбрасывается, если было взятие или ход пешкой.
В остальных случаях счётчик увеличивается на 1 после каждого полухода.
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
        self.next_move = fen.split()[1][0].lower()
        self.castling = self.check_castling(fen.split()[2])
        self.passant = fen.split()[3]
        self.halfmoves = int(fen.split()[4])
        self.fullmoves = int(fen.split()[5])

    @staticmethod
    def check_castling(line):
        template = "KQkq"
        new_line = ""
        for c in template:
            if c in line:
                new_line += c
        return new_line if new_line else "-"

    def __str__(self):
        return ' '.join([self.matrix_figures_str_fen(), self.next_move,
                         self.castling, self.passant, str(self.halfmoves), str(self.fullmoves)])

    def parse_location_figures(self):
        """парсит положение фигур - возвращает list строк позиций"""
        location_figures = self.figures.split('/')
        for y in range(len(location_figures)):
            row = location_figures[y]
            new_row = ''
            for k in row:
                if k.isdigit():
                    new_row += '.' * int(k)
                elif k in 'rnbqkbnrpRNBQKBNRP':
                    new_row += k
            if len(new_row) < 9:
                new_row += '.' * (8 - len(new_row))
            location_figures[y] = new_row
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

    def print_chess_board(self):
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
                board_matrix[i + 1][j + 4 + f] = self.matrix_figures()[i][j]
                f += 1

        """plot board wirh figures"""
        for i in range(11):
            print(*board_matrix[i], sep='')

    def make_move(self, move):
        if move:
            if self.next_move == 'w':
                self.next_move = 'b'
                if self.get_move_figure(move)[0].lower() == 'p' or self.get_move_figure(move)[2] != '.':
                    self.halfmoves = 0
                else:
                    self.halfmoves += 1
            else:
                self.next_move = 'w'
                self.fullmoves += 1
                if self.get_move_figure(move)[0].lower() == 'p' or self.get_move_figure(move)[2] != '.':
                    self.halfmoves = 0
                else:
                    self.halfmoves += 1

    def get_move_figure(self, move):
        horizontal = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
        vertical = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        figure = self.matrix_figures()[horizontal[move[1]]][vertical[move[0]]]
        figure_start_position = self.matrix_figures()[horizontal[move[1]]][vertical[move[0]]]
        figure_end_position = self.matrix_figures()[horizontal[move[3]]][vertical[move[2]]]
        return figure, figure_start_position, figure_end_position


if __name__ == "__main__":
    fen = input(str())  # inpput fen notation
    move = input(str())  # input move
    chess1 = Chess(fen)
    chess1.make_move(move)
    print(chess1)
