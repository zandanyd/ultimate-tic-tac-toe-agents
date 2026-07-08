import math
import copy


class MinimaxAgent:
    def __init__(self, player_id, depth=3):
        """
        Initialize the Minimax Agent.
        player_id: 1 for 'X', -1 for 'O'
        depth: The maximum depth for the search tree
        """
        self.player_id = player_id
        self.depth = depth

    def get_best_move(self, env):
        valid_moves = env.get_valid_moves()

        if not valid_moves:
            return None
        if len(valid_moves) == 1:
            return valid_moves[0]

        best_move = None
        alpha = -math.inf
        beta = math.inf

        if self.player_id == 1:
            best_score = -math.inf
            for move in valid_moves:
                env_copy = copy.deepcopy(env)
                env_copy.make_move(move[0], move[1])
                score = self.minimax(env_copy, self.depth - 1, alpha, beta, False)
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        else:
            best_score = math.inf
            for move in valid_moves:
                env_copy = copy.deepcopy(env)
                env_copy.make_move(move[0], move[1])
                score = self.minimax(env_copy, self.depth - 1, alpha, beta, True)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break

        return best_move

    def minimax(self, env, depth, alpha, beta, is_maximizing):
        game_status = self.check_global_win(env)
        if game_status != 0:
            return game_status * 10000

        if depth == 0:
            return self.evaluate_board(env)

        valid_moves = env.get_valid_moves()
        if not valid_moves:
            return self.evaluate_board(env)

        if is_maximizing:
            max_eval = -math.inf
            for move in valid_moves:
                env_copy = copy.deepcopy(env)
                env_copy.make_move(move[0], move[1])
                eval_score = self.minimax(env_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in valid_moves:
                env_copy = copy.deepcopy(env)
                env_copy.make_move(move[0], move[1])
                eval_score = self.minimax(env_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def check_global_win(self, env):
        b = env.macro_board
        for i in range(3):
            if abs(b[i][0] + b[i][1] + b[i][2]) == 3: return b[i][0]
            if abs(b[0][i] + b[1][i] + b[2][i]) == 3: return b[0][i]
        if abs(b[0][0] + b[1][1] + b[2][2]) == 3: return b[0][0]
        if abs(b[0][2] + b[1][1] + b[2][0]) == 3: return b[0][2]
        return 0

    def evaluate_lines(self, grid, start_r, start_c):
        """
        Helper function to evaluate rows, columns, and diagonals in a 3x3 grid.
        Rewards 2-in-a-row (with an empty 3rd slot) and blocks.
        Positive score means advantage for Player 1, negative for Player -1.
        """
        score = 0
        lines = [
            [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],  # Rows
            [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],  # Cols
            [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]  # Diagonals
        ]

        for line in lines:
            p1_count = 0
            p2_count = 0
            for dr, dc in line:
                val = grid[start_r + dr][start_c + dc]
                if val == 1:
                    p1_count += 1
                elif val == -1:
                    p2_count += 1

            # Unblocked lines (potential wins)
            if p1_count > 0 and p2_count == 0:
                if p1_count == 2:
                    score += 10
                elif p1_count == 1:
                    score += 1
            elif p2_count > 0 and p1_count == 0:
                if p2_count == 2:
                    score -= 10
                elif p2_count == 1:
                    score -= 1

        return score

    def evaluate_board(self, env):
        score = 0

        # 1. Evaluate Macro Board (Completed boards and global threats)
        for r in range(3):
            for c in range(3):
                macro_val = env.macro_board[r][c]
                if macro_val == 1:
                    score += 100
                elif macro_val == -1:
                    score -= 100
                if macro_val != 0 and r == 1 and c == 1:
                    score += (macro_val * 50)

        # Huge reward for setting up 2-in-a-row of won macro boards
        score += self.evaluate_lines(env.macro_board, 0, 0) * 100

        # 2. Evaluate Micro Boards (Individual cells and local threats)
        for macro_r in range(3):
            for macro_c in range(3):
                if env.macro_board[macro_r][macro_c] == 0:
                    # Bonus for center/corners
                    cell_val = env.board[macro_r * 3 + 1][macro_c * 3 + 1]
                    score += cell_val * 5
                    for dr, dc in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                        score += env.board[macro_r * 3 + dr][macro_c * 3 + dc] * 2

                        # Reward 2-in-a-rows and blocking in this specific small board
                    score += self.evaluate_lines(env.board, macro_r * 3, macro_c * 3) * 5

        # 3. ADVANCED TACTICS: Penalize bad board positioning

        # A. The "Free Move" Penalty
        if env.next_macro_row == -1:
            # The active player is getting a free move, which is great for them
            score += 40 if env.current_player == 1 else -40

        # B. Target Board Danger Penalty
        else:
            # The active player is FORCED to play in this board.
            # Are they close to winning it?
            target_r = env.next_macro_row
            target_c = env.next_macro_col
            if env.macro_board[target_r][target_c] == 0:
                lines_score = self.evaluate_lines(env.board, target_r * 3, target_c * 3)

                # If it's Player 1's turn and Player 1 is doing great in that board, big bonus
                if env.current_player == 1 and lines_score > 0:
                    score += 20
                    # If it's Player -1's turn and Player -1 is doing great in that board, big penalty
                elif env.current_player == -1 and lines_score < 0:
                    score -= 20

        return score