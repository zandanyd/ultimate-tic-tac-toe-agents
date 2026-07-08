class UltimateTicTacToe:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]

        self.macro_board = [[0] * 3 for _ in range(3)]

        self.current_player = 1  #

        self.next_macro_row = -1
        self.next_macro_col = -1

    def get_valid_moves(self):
        moves = []
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    macro_r, macro_c = r // 3, c // 3

                    if (self.next_macro_row == -1 and self.macro_board[macro_r][macro_c] == 0) or \
                            (self.next_macro_row == macro_r and self.next_macro_col == macro_c and
                             self.macro_board[macro_r][macro_c] == 0):
                        moves.append((r, c))
        return moves

    def make_move(self, r, c):
        if (r, c) not in self.get_valid_moves():
            return False

        self.board[r][c] = self.current_player
        macro_r, macro_c = r // 3, c // 3

        if self.check_local_win(macro_r, macro_c):
            self.macro_board[macro_r][macro_c] = self.current_player
        elif self.is_local_board_full(macro_r, macro_c):
            self.macro_board[macro_r][macro_c] = 2

        next_r_target, next_c_target = r % 3, c % 3

        if self.macro_board[next_r_target][next_c_target] != 0:
            self.next_macro_row, self.next_macro_col = -1, -1
        else:
            self.next_macro_row, self.next_macro_col = next_r_target, next_c_target

        self.current_player *= -1
        return True

    def check_local_win(self, macro_r, macro_c):
        start_r, start_c = macro_r * 3, macro_c * 3
        b = self.board
        p = self.current_player

        for i in range(3):
            if all(b[start_r + i][start_c + j] == p for j in range(3)) or \
                    all(b[start_r + j][start_c + i] == p for j in range(3)):
                return True

        if all(b[start_r + i][start_c + i] == p for i in range(3)) or \
                all(b[start_r + i][start_c + 2 - i] == p for i in range(3)):
            return True

        return False

    def is_local_board_full(self, macro_r, macro_c):
        start_r, start_c = macro_r * 3, macro_c * 3
        for i in range(3):
            for j in range(3):
                if self.board[start_r + i][start_c + j] == 0:
                    return False
        return True