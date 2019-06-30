"""
Условие задачи

KQkq — возможны короткие и длинные рокировки белых и чёрных

Дана FEN-позиция и ход.
Это может быть любой ход, кроме рокировки.
Если это ход ладьёй - необходимо убрать флаг рокировки для этого игрока в сторону этой ладьи.
Если это ход королём - необходимо убрать флаг рокировки для этого игрока.
Если это взятие ладьи - необходимо убрать флаг рокировки для взятой ладьи.

Необходимо выполнить ход и передать право хода.
Делать проверку на возможность хода не нужно.

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
        self.matrix = self.matrix_figures()
        self.moving_figure = self.get_move_figure(move)
        self.bit_figure = self.get_bit_figure(move)

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
        for row in self.matrix:
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
                board_matrix[i + 1][j + 4 + f] = self.matrix[i][j]
                f += 1

        """plot board wirh figures"""
        for i in range(11):
            print(*board_matrix[i], sep='')

    def make_move(self, move):
        if move:
            a1 = self.get_move_figure(move)
            horizontal = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
            vertical = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
            figure = self.matrix[horizontal[move[1]]][vertical[move[0]]]
            current_player = self.next_move
            figure_start_position = self.matrix[horizontal[move[1]]][vertical[move[0]]]
            figure_end_position = self.matrix[horizontal[move[3]]][vertical[move[2]]]
            self.matrix[horizontal[move[1]]][vertical[move[0]]] = '.'
            self.matrix[horizontal[move[3]]][vertical[move[2]]] = figure
            self.next_color_halfmoves(figure,figure_start_position, figure_end_position)
            self.check_castling_2(move)


        return figure, figure_start_position, figure_end_position, current_player, self.castling


    def next_color_halfmoves(self, figure, figure_start_position, figure_end_position):

        if self.next_move == 'w':
            self.next_move = 'b'
            if figure.lower() == 'p' or figure_end_position != '.':
                self.halfmoves = 0
            else:
                self.halfmoves += 1
        else:
            self.next_move = 'w'
            self.fullmoves += 1
            if figure.lower() == 'p' or figure_end_position != '.':
                self.halfmoves = 0
            else:
                self.halfmoves += 1
        return self.next_move, self.halfmoves

    def check_castling_2(self, move):
        if move:
            if self.moving_figure == 'k':
                if 'k' in self.castling:
                    self.castling =self.castling[0:self.castling.index('k')]
            elif self.moving_figure == 'K':
                if 'KQ' in self.castling:
                    self.castling = self.castling[self.castling.index('K')+2:]
                if 'K' in self.castling:
                    self.castling = self.castling[self.castling.index('K') + 1:]
            elif self.moving_figure == 'r':
                if move[:2] == 'a8':
                    if 'q' in self.castling:
                        self.castling = self.castling[0:self.castling.index('q')]
                if move[:2] == 'h8':
                    if 'k' in self.castling:
                        self.castling = self.castling[0:self.castling.index('k')] + self.castling[self.castling.index('k')+1:]
            elif self.moving_figure == 'R':
                if move[:2] == 'a1':
                    if 'Q' in self.castling:
                        self.castling = self.castling[0:self.castling.index('Q')]+ self.castling[self.castling.index('Q')+1:]
                if move[:2] == 'h1':
                    if 'K' in self.castling:
                        self.castling = self.castling[0:self.castling.index('K')] + self.castling[self.castling.index('K')+1:]
            elif self.bit_figure == 'r':
                if move[2:4] == 'a8':
                    if 'q' in self.castling:
                        self.castling = self.castling[0:self.castling.index('q')]
                if move[2:4] == 'h8':
                    if 'k' in self.castling:
                        self.castling = self.castling[0:self.castling.index('k')] + self.castling[self.castling.index('k')+1:]
            elif self.bit_figure == 'R':
                if move[2:4] == 'a1':
                    if 'Q' in self.castling:
                        self.castling = self.castling[0:self.castling.index('Q')]+ self.castling[self.castling.index('Q')+1:]
                if move[2:4] == 'h1':
                    if 'K' in self.castling:
                        self.castling = self.castling[self.castling.index('K')+1:]

        return self.castling

    def get_bit_figure(self, move):
        if move:
            horizontal = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
            vertical = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
            self.bit_figure = self.matrix[horizontal[move[3]]][vertical[move[2]]]
        return self.bit_figure


    def get_move_figure (self, move):
        if move:
            horizontal = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
            vertical = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
            self.moving_figure = self.matrix[horizontal[move[1]]][vertical[move[0]]]
        return self.moving_figure

if __name__ == "__main__":
    fen = input(str())  # inpput fen notation
    move = input(str())  # input move
    chess1 = Chess(fen)
    # chess1.get_move_figure(move)
    chess1.get_move_figure(move)
    chess1.make_move(move)
    print(chess1)
    print(chess1.print_chess_board())
    print('moving_figure - ',chess1.moving_figure)
    # print( 'current_player ' ,chess1.make_move(move)[3])

