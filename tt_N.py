class Notation:
    def __init__(self, feNotation):
        def_lst = ["8/8/8/8/8/8/8/8", "w", "-", "-", "0", "1"]  #
        if feNotation:
            lst = feNotation.split(" ")
            for i, l in enumerate(lst):
                def_lst[i] = l
        self.board = None
        self.fill_board(def_lst[0])
        self.is_white_next_move = def_lst[1].lower() == "w"
        self.castling = self.check_castling(def_lst[2])
        self.passant = def_lst[3]
        self.halfMoves = int(def_lst[4])
        self.fullMoves = int(def_lst[5])
        self.figureList = "PNBRQK"

    def __str__(self):
        return self.board_string() + " " + ('w' if self.is_white_next_move else 'b') + " " + self.castling + " " + \
               self.passant + " " + str(self.halfMoves) + " " + str(self.fullMoves)

    @staticmethod
    def count_moves(moves):
        result = 0
        for move in moves:
            lst = move.split(" ")
            result += len(lst)
        return result

    @staticmethod
    def sorted_and_grouped(lines):
        lines.sort()
        grouped = list()
        group_prefix = ""
        new_line = ""

        for line in lines:
            prefix = line[:2]
            if prefix == group_prefix:
                new_line += " " + line
            else:
                if group_prefix:
                    grouped.append(new_line)
                new_line = line
                group_prefix = prefix

        if group_prefix:
            grouped.append(new_line)

        return grouped

    @staticmethod
    def check_castling(line):
        template = "KQkq"
        new_line = ""
        for c in template:
            if c in line:
                new_line += c
        return new_line if new_line else "-"

    def board_string(self):
        new_board = list()
        for line in self.board:
            new_line = ""
            dots_count = 0
            for c in line:
                if c == '.':
                    dots_count += 1
                else:
                    if dots_count > 0:
                        new_line += str(dots_count)
                        dots_count = 0
                    new_line += c
            if dots_count > 0:
                new_line += str(dots_count)
            new_board.append(new_line)
        return "/".join(new_board)

    def fill_board(self, lines):
        self.board = lines.split("/")
        for i, line in enumerate(self.board):
            new_line = ""
            for c in line:
                if c.lower() in "rnbqkp":
                    new_line += c
                elif c in "12345678":
                    new_line += '.' * int(c)
                else:
                    new_line += "x"
            new_line += '.' * (8 - len(new_line))
            self.board[i] = new_line

    def print_board(self):
        print("  +-----------------+")
        for i, line in enumerate(self.board):
            print(f'{8 - i} | {" ".join(line)} |')
        print("  +-----------------+")
        print("    a b c d e f g h  ")

    def get_bitboard(self):
        bit_pieces = "PNBRQKpnbrqk"
        bit_board = {c: 0 for c in bit_pieces}
        i = 1
        for c in "".join(reversed(self.board)):
            if c != ".":
                bit_board[c] += i
            i *= 2
        return bit_board

    def make_move(self, move):
        if move:
            self.is_white_next_move = not self.is_white_next_move
            if self.is_white_next_move: self.fullMoves += 1
            start_cell = move[:2]
            bitten_cell = move[2:4]
            moving_figure = self.get_figure_at(start_cell);
            bitten_figure = self.get_figure_at(bitten_cell);
            if moving_figure.lower() != 'p' and bitten_figure == '.':
                self.halfMoves += 1
            else:
                self.halfMoves = 0

            if start_cell == "e1":
                if moving_figure == 'K':
                    self.remove_from_castling('K')
                    self.remove_from_castling('Q')
                    if bitten_cell == "g1":
                        self.set_cell_with("h1", '.')
                        self.set_cell_with("f1", 'R')
                    elif bitten_cell == "c1":
                        self.set_cell_with("a1", '.')
                        self.set_cell_with("d1", 'R')
            elif start_cell == "e8":
                if moving_figure == 'k':
                    self.remove_from_castling('k')
                    self.remove_from_castling('q')
                    if bitten_cell == "g8":
                        self.set_cell_with("h8", '.')
                        self.set_cell_with("f8", 'r')
                    elif bitten_cell == "c8":
                        self.set_cell_with("a8", '.')
                        self.set_cell_with("d8", 'r')

            if start_cell == "a8":
                if moving_figure == 'r':
                    self.remove_from_castling('q')
            elif start_cell == "h8":
                if moving_figure == 'r':
                    self.remove_from_castling('k')
            elif start_cell == "a1":
                if moving_figure == 'R':
                    self.remove_from_castling('Q')
            elif start_cell == "h1":
                if moving_figure == 'R':
                    self.remove_from_castling('K')

            if bitten_cell == "a8":
                if bitten_figure == 'r':
                    self.remove_from_castling('q')
            elif bitten_cell == "h8":
                if bitten_figure == 'r':
                    self.remove_from_castling('k')
            elif bitten_cell == "a1":
                if bitten_figure == 'R':
                    self.remove_from_castling('Q')
            elif bitten_cell == "h1":
                if bitten_figure == 'R':
                    self.remove_from_castling('K')

            if len(move) == 5:
                if self.is_white_next_move:
                    moving_figure = move[4].lower()
                else:
                    moving_figure = move[4].upper()

            if bitten_cell == self.passant and moving_figure.lower() == 'p':
                self.set_cell_with(bitten_cell[:1] + start_cell[1:], '.')
            self.passant = "-"
            if moving_figure.lower() == 'p':
                if (self.get_row(start_cell) - self.get_row(bitten_cell)) * (
                        -1 if self.is_white_next_move else 1) == 2:
                    alien_figure = 'P' if moving_figure == 'p' else 'p'
                    if self.get_figure_at_left(bitten_cell) == alien_figure or self.get_figure_at_right(
                            bitten_cell) == alien_figure:
                        self.passant = start_cell[0] + ('6' if self.is_white_next_move else '3')

            self.set_cell_with(start_cell, '.')
            self.set_cell_with(bitten_cell, moving_figure)

    def get_figure_at_left(self, cell):
        if self.get_column(cell) == 0:
            return self.get_figure_at(cell)
        else:
            return self.board[self.get_row(cell)][self.get_column(cell) - 1]

    def get_figure_at_right(self, cell):
        if self.get_column(cell) == 7:
            return self.get_figure_at(cell)
        else:
            return self.board[self.get_row(cell)][self.get_column(cell) + 1]

    def get_figure_at(self, cell):
        return self.board[self.get_row(cell)][self.get_column(cell)]

    def set_cell_with(self, cell, c):
        j = self.get_column(cell)
        self.board[self.get_row(cell)] = self.board[self.get_row(cell)][:j] + c + self.board[self.get_row(cell)][j + 1:]

    def remove_from_castling(self, c):
        if c in self.castling:
            j = self.castling.index(c)
            self.castling = self.castling[:j] + self.castling[j + 1:]
            if len(self.castling) == 0:
                self.castling = "-"

    def generate_all_moves(self, figures=None):
        if not figures:
            figures = self.figureList
        return self.generate_moves(figures if self.is_white_next_move else figures.lower())

    def generate_moves(self, figures):
        generate_moves_for = {'p': self.moves_pawn_from,
                              'n': self.moves_knight_from,
                              'b': self.moves_bishop_from,
                              'r': self.moves_rook_from,
                              'q': self.moves_queen_from,
                              'k': self.moves_king_from}
        moves = list()
        for figure in figures:
            positions = self.get_figure_positions(figure)
            for position in positions:
                moves_from_position = generate_moves_for[figure.lower()](position)
                if moves_from_position:
                    moves.append(moves_from_position)
        return moves

    def can_ocupy(self, bitten_figure):
        return (bitten_figure == '.') or \
               (self.is_white_next_move and (bitten_figure == bitten_figure.lower())) or \
               (not self.is_white_next_move and bitten_figure == bitten_figure.upper())

    @staticmethod
    def get_string_from_list(moves):
        result = ""
        moves.sort()
        if moves:
            result = " ".join(moves)
        return result

    def moves_pawn_from(self, position):
        return ""

    def moves_knight_from(self, position):
        pos_i = self.get_row(position)
        pos_j = self.get_column(position)
        moves = list()
        d_i, d_j = 2, 1
        s_i, s_j = 1, 1
        for i in range(4):
            for j in range(2):
                move_to = self.get_cell_name(pos_i + d_i * s_i, pos_j + d_j * s_j)
                if move_to:
                    bitten_figure = self.get_figure_at(move_to)
                    # free cell - add to list
                    # occupied cell - check for enemy
                    # if white next move and bitten figure is black(lowercase)
                    # or not white next move and bitten figure is white(uppercase)
                    # bittenFigure is enemy - add to list
                    if self.can_ocupy(bitten_figure):
                        moves.append(position + move_to)
                d_i, d_j = d_j, d_i
            if i == 1: s_i = -s_i
            s_j = -s_j
        return self.get_string_from_list(moves)

    def moves_bishop_from(self, position):
        return ""

    def moves_rook_from(self, position):
        return ""

    def moves_queen_from(self, position):
        return ""

    def moves_king_from(self, position):
        return ""

    def get_figure_positions(self, figure):
        positions = list()
        for j in range(8):
            for i in range(7, -1, -1):
                if self.board[i][j] == figure:
                    positions.append(self.get_cell_name(i, j))
        return positions

    @staticmethod
    def get_cell_name(i, j):
        if i < 0 or i > 7 or j < 0 or j > 7:
            return ""
        else:
            return chr(ord('a') + j) + chr(8 - i + ord('0'))

    @staticmethod
    def get_column(cell):
        return ord(cell[0]) - ord("a")

    @staticmethod
    def get_row(cell):
        return 8 - int(cell[1])


line = input()
notation = Notation(line)
moves = notation.generate_all_moves("N")
moves.sort()
count = Notation.count_moves(moves)
print(count)
for move in moves:
    print(move)