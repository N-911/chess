"""Условие задачи
Дана позиция, в которой могут быть белые и/или чёрные слоны.
Необходимо сгенерировать все возможные ходы слонами для той стороны, чей сейчас ход.

Слон ходит по диагонали на одно или несколько полей,
он не может перепрыгивать фигуры,
может ходить на пустое поле в прямой видимости
или делать взятие на поле с фигурой противника.
Проверку на шах делать не нужно.

Дано: FEN-позиция.
Надо: Вывести количество ходов и их список.
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
        self.matrix_moves = self.generate_matrix_moves()[0]
        # self.moving_figure = self.get_move_figure(move)
        self.moving_figure = []
        self.list_moves = self.generate_matrix_moves()[1]
        self.bit_figure = None

    horizontal = {'8': 0, '7': 1, '6': 2, '5': 3, '4': 4, '3': 5, '2': 6, '1': 7}
    vertical = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    castling_d = ['e1g1', 'e1c1', 'e8g8', 'e8c8']


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
                         self.castling if len(self.castling) > 0 else '-', self.passant, str(self.halfmoves), str(self.fullmoves)])

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
            figure = self.matrix[self.horizontal[move[1]]][self.vertical[move[0]]]
            current_player = self.next_move
            figure_start_position = self.matrix[self.horizontal[move[1]]][self.vertical[move[0]]]
            figure_end_position = self.matrix[self.horizontal[move[3]]][self.vertical[move[2]]]
            self.matrix[self.horizontal[move[1]]][self.vertical[move[0]]] = '.'
            self.matrix[self.horizontal[move[3]]][self.vertical[move[2]]] = figure
            self.next_color_halfmoves(figure, figure_start_position, figure_end_position)
            self.check_castling_2(move)
            if len(move) == 5:
                self.pawn_turn(move)  # преобразование пешки в фигуру

            if self.moving_figure.lower() == 'k' and move in self.castling_d:
                rook = 'r' if self.next_move == 'w' else 'R'
                if self.vertical[move[0]] > self.vertical[move[2]]:
                    self.matrix[self.horizontal[move[1]]][self.vertical['a']] = '.'
                    self.matrix[self.horizontal[move[1]]][self.vertical['d']] = rook

                if self.vertical[move[0]] < self.vertical[move[2]]:
                    self.matrix[self.horizontal[move[1]]][self.vertical['h']] = '.'
                    self.matrix[self.horizontal[move[1]]][self.vertical['f']] = rook
        else:
            pass


        return figure, figure_start_position, figure_end_position, current_player, self.castling, self.passant

    def generate_all_moves(self):

        figures = 'RNBKQ' if self.next_move =='w' else 'rnbkq'

        figures_position = {x : self.get_position(x) for x in figures }
        list_moves = []
        for el in figures:

            if el == 'N' or el == 'n':
                ll = figures_position[el]
                for i in ll:
                    list_moves+=(self.generate_knights_moves(i))
            else:
                pass

        return sorted(list_moves)

    def sorted_list_moves(self):
        list_moves = self.generate_all_moves()
        all = []
        sorted_list =[]
        if len(list_moves) > 0:
            sorted_list.append(list_moves[0])
            for i in range(1, len(list_moves)):
                if list_moves[i][:2] == list_moves[i - 1][:2]:
                    sorted_list.append(list_moves[i])
                else:
                    all.append(sorted_list)
                    sorted_list =list()
                    sorted_list.append(list_moves[i])
            all.append(sorted_list)
        return all

    def get_position(self, x):
        """ позиции фигуры """
        list_f = []
        for i in range(8):
            for j in range(8):
                if self.matrix[i][j] == x:
                    list_f.append([i,j])
        return list_f


    def generate_knights_moves (self, figure_position):          # list [0,1]
        moves_n = [(-2, 1), (-1,2), (1,2),(2,1),(2,-1), (1, -2), (-1, -2),(-2,-1)]
        enemy_figures = 'PRNBKQ' if self.next_move == 'b' else 'rnbkq'
        matrix = [['.'] * 8 for x in range(8)]
        # figure_position = [7,1]
        figure_position_fen = self.get_key(Chess.vertical, figure_position[1]) + self.get_key(Chess.horizontal,figure_position[0])
        moves_list =[]
        for i in range(8):
            x = figure_position[0] + moves_n[i][0]
            y = figure_position[1] + moves_n[i][1]
            if (0 <= x < 8) and (0 <= y < 8):
                # matrix [x][y] = "N"
                # if self.matrix[x][y] == '.' or self.matrix[x][y] in 'PRNBKQ' if self.next_move == 'b' else 'rnbkq':
                if self.matrix[x][y] not in 'PRNBKQ' if self.next_move == 'w' else 'rnbkq':
                    moves_list.append( figure_position_fen + self.get_key(Chess.vertical, y) + self.get_key(Chess.horizontal, x))

        return  sorted(moves_list)

    def generate_matrix_moves(self):
        moves_n = [(-2, 1), (-1,2), (1,2),(2,1),(2,-1), (1, -2), (-1, -2),(-2,-1)]
        matrix = [['.'] * 8 for x in range(8)]
        figure_position = [7,6]
        figure_position_fen = self.get_key(Chess.vertical, figure_position[1]) + self.get_key(Chess.horizontal,figure_position[0])
        matrix[figure_position[0]][figure_position[1]] = '+'
        aa =[]
        for i in range(8):
            x = figure_position[0] + moves_n[i][0]
            y = figure_position[1] + moves_n[i][1]
            if (0 <= x < 8) and (0 <= y < 8):
                matrix [x][y] = "N"
                aa.append( figure_position_fen + self.get_key(Chess.vertical, y) + self.get_key(Chess.horizontal, x))


        return matrix, aa


    def get_key (self,dict, value):
        for key, val in dict.items():
            if val == value:
                return key

    def print_generate_matrix_moves(self):
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
                board_matrix[i + 1][j + 4 + f] = self.matrix_moves[i][j]
                f += 1

        """plot board wirh figures"""
        for i in range(11):
            print(*board_matrix[i], sep='')


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
                    self.castling = self.castling[0:self.castling.index('k')]
            elif self.moving_figure == 'K':
                if 'KQ' in self.castling:
                    self.castling = self.castling[self.castling.index('K') + 2:]
                if 'K' in self.castling:
                    self.castling = self.castling[self.castling.index('K') + 1:]
            elif self.moving_figure == 'r':
                if move[:2] == 'a8':
                    if 'q' in self.castling:
                        self.castling = self.castling[0:self.castling.index('q')]
                if move[:2] == 'h8':
                    if 'k' in self.castling:
                        self.castling = self.castling[0:self.castling.index('k')] + self.castling[
                                                                                    self.castling.index('k') + 1:]
            elif self.moving_figure == 'R':
                if move[:2] == 'a1':
                    if 'Q' in self.castling:
                        self.castling = self.castling[0:self.castling.index('Q')] + self.castling[
                                                                                    self.castling.index('Q') + 1:]
                if move[:2] == 'h1':
                    if 'K' in self.castling:
                        self.castling = self.castling[0:self.castling.index('K')] + self.castling[
                                                                                    self.castling.index('K') + 1:]
            elif self.bit_figure == 'r':
                if move[2:4] == 'a8':
                    if 'q' in self.castling:
                        self.castling = self.castling[0:self.castling.index('q')]
                if move[2:4] == 'h8':
                    if 'k' in self.castling:
                        self.castling = self.castling[0:self.castling.index('k')] + self.castling[
                                                                                    self.castling.index('k') + 1:]
            elif self.bit_figure == 'R':
                if move[2:4] == 'a1':
                    if 'Q' in self.castling:
                        self.castling = self.castling[0:self.castling.index('Q')] + self.castling[
                                                                                    self.castling.index('Q') + 1:]
                if move[2:4] == 'h1':
                    if 'K' in self.castling:
                        self.castling = self.castling[self.castling.index('K') + 1:]

        return self.castling

    def get_bit_figure(self, move):
        if move:
            self.bit_figure = self.matrix[self.horizontal[move[3]]][self.vertical[move[2]]]


        return self.bit_figure

    def get_move_figure(self, move):
        if move:
            self.moving_figure = self.matrix[self.horizontal[move[1]]][self.vertical[move[0]]]
        return self.moving_figure

    def pawn_turn(self, move):

        """превращение пешки у фигуру которая передается в позиции 5 хода """

        self.moving_figure = move[4]
        self.matrix[self.horizontal[move[3]]][self.vertical[move[2]]] = self.moving_figure
        return self.moving_figure, self.matrix

    def set_passant(self, move):

        """установить признак "битового поля", если рядом есть пешка противника"""

        if self.passant == '-' and self.moving_figure == 'P':
            if self.matrix[self.horizontal[move[3]]][self.vertical[move[2]] - 1] == 'p' or \
                    self.matrix[self.horizontal[move[3]]][self.vertical[move[2]] + 1] == 'p':
                if move[1] == '2' and move[3] == '4':
                    self.passant = move[0] + '3'
            else:
                self.passant = '-'
        elif self.passant == '-' and self.moving_figure == 'p':
            if self.matrix[self.horizontal[move[3]]][self.vertical[move[2]] - 1] == 'P' or \
                    self.matrix[self.horizontal[move[3]]][self.vertical[move[2]] + 1] == 'P':
                if move[1] == '7' and move[3] == '5':
                    self.passant = move[0] + '6'
            else:
                self.passant = '-'
        elif self.passant == move[2:4]:
            if self.moving_figure == 'P':
                self.matrix[self.horizontal[move[1]]][self.vertical[move[2]]] = '.'
                self.passant = '-'
            elif self.moving_figure == 'p':
                self.matrix[self.horizontal[move[1]]][self.vertical[move[2]]] = '.'
                self.passant = '-'
        elif self.passant != '-' and self.moving_figure == 'P':
            if self.matrix[self.horizontal[move[3]]][self.vertical[move[2]] - 1] == 'p' or \
                    self.matrix[self.horizontal[move[3]]][self.vertical[move[2]] + 1] == 'p':
                if move[1] == '2' and move[3] == '4':
                    self.passant = move[0] + '3'
            else:
                self.passant = '-'
        elif self.passant != '-' and self.moving_figure == 'p':
            if self.matrix[self.horizontal[move[3]]][self.vertical[move[2]] - 1] == 'P' or \
                    self.matrix[self.horizontal[move[3]]][self.vertical[move[2]] + 1] == 'P':
                if move[1] == '7' and move[3] == '5':
                    self.passant = move[0] + '6'
            else:
                self.passant = '-'

        return self.passant, self.matrix

if __name__ == "__main__":
    # fen = input(str())  # inpput fen notation
    # move = input(str())  # input move
    fen ="r2qk2r/ppp2ppp/2np1n2/2bNp1B1/2B1P1b1/3P1N2/PPP2PPP/R2QK2R b KQkq - 3 7"
    move =None
    chess1 = Chess(fen)
    if move:
        chess1.get_move_figure(move)
        chess1.set_passant(move)  # Взятие на проходе
        chess1.make_move(move)
    print(chess1.print_chess_board())
    # print(chess1.print_generate_matrix_moves())
    # print(sorted(chess1.get_position('n')))
    print(len(chess1.generate_all_moves()))
    # print(*chess1.generate_all_moves())
    # print(chess1.generate_knights_moves())
    # for i in range(len(chess1.sorted_list_moves())):
    #     print(*chess1.sorted_list_moves()[i])
    result = chess1.sorted_list_moves()
    for _ in result:
        print(*_)