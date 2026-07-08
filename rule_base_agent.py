import random
import copy


class RuleBasedAgent:
    def __init__(self, player_id):
        self.player_id = player_id

    def get_best_move(self, env):
        valid_moves = env.get_valid_moves()
        if not valid_moves:
            return None
        # Rule 1: Can I win a small board right now?
        for move in valid_moves:
            env_copy = copy.deepcopy(env)
            env_copy.make_move(move[0], move[1])
            macro_r, macro_c = move[0] // 3, move[1] // 3
            if env_copy.macro_board[macro_r][macro_c] == self.player_id:
                return move

        # Rule 2: Can I block the opponent from winning a small board?
        opponent_id = -self.player_id
        for move in valid_moves:
            env_copy = copy.deepcopy(env)
            env_copy.current_player = opponent_id
            env_copy.make_move(move[0], move[1])
            macro_r, macro_c = move[0] // 3, move[1] // 3
            if env_copy.macro_board[macro_r][macro_c] == opponent_id:
                return move

        # Rule 3: Prefer the center of the small board
        for move in valid_moves:
            if move[0] % 3 == 1 and move[1] % 3 == 1:
                return move

        return random.choice(valid_moves)