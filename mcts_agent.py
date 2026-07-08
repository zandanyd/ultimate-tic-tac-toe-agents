import math
import random
import copy
from minmax_agent import MinimaxAgent


class MCTSNode:
    def __init__(self, env, parent=None, move=None):
        self.env = env
        self.parent = parent
        self.move = move  # The move that led to this node
        self.children = []
        self.wins = 0.0
        self.visits = 0
        self.untried_moves = env.get_valid_moves()
        # The player who made the move to reach this state
        self.player_who_just_moved = -env.current_player

    def uct_select_child(self):
        """
        Selects a child node using the UCB1 formula (Upper Confidence Bound).
        Balances exploitation (high win rate) and exploration (low visits).
        """
        best_child = max(self.children,
                         key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))
        return best_child

    def add_child(self, move, env):
        """
        Expands the tree by adding a new child node for the given move.
        """
        child = MCTSNode(env, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        """
        Backpropagates the result of a simulation up the tree.
        """
        self.visits += 1
        self.wins += result


class MCTSAgent:
    def __init__(self, player_id, iterations=500, use_heuristic=False):
        """
        player_id: 1 for 'X', -1 for 'O'
        iterations: Number of simulations to run per move
        use_heuristic: If True, uses the Minimax heuristic instead of simulating to the end
        """
        self.player_id = player_id
        self.iterations = iterations
        self.use_heuristic = use_heuristic

        # We initialize a dummy Minimax agent just to reuse its evaluation functions
        self.evaluator = MinimaxAgent(player_id=1, depth=1)

    def get_best_move(self, env):
        root = MCTSNode(copy.deepcopy(env))

        if not root.untried_moves:
            return None
        if len(root.untried_moves) == 1:
            return root.untried_moves[0]

        print(
            f"MCTS Agent {self.player_id} is thinking... (Iterations: {self.iterations}, Heuristic: {self.use_heuristic})")

        for _ in range(self.iterations):
            node = root
            state = copy.deepcopy(env)

            # 1. SELECTION: Traverse down the tree to a leaf node
            while not node.untried_moves and node.children:
                node = node.uct_select_child()
                state.make_move(node.move[0], node.move[1])

            # 2. EXPANSION: Expand the leaf node if possible
            if node.untried_moves:
                move = random.choice(node.untried_moves)
                state.make_move(move[0], move[1])
                node = node.add_child(move, copy.deepcopy(state))

            # 3. SIMULATION (Rollout)
            # If using heuristic, we don't simulate to the end of the game (too deep).
            # We simulate 15 random moves and then evaluate the board.
            max_depth = 15 if self.use_heuristic else 100
            depth = 0

            while state.get_valid_moves() and self.evaluator.check_global_win(state) == 0 and depth < max_depth:
                possible_moves = state.get_valid_moves()
                m = random.choice(possible_moves)
                state.make_move(m[0], m[1])
                depth += 1

            # 4. BACKPROPAGATION: Send the result back up the tree
            result = self.get_result(state)

            curr_node = node
            while curr_node is not None:
                # If the node represents a move made by our agent, it gets the points.
                # Otherwise, the opponent gets the inverted points.
                if curr_node.player_who_just_moved == self.player_id:
                    curr_node.update(result)
                else:
                    curr_node.update(1.0 - result)
                curr_node = curr_node.parent

        # Choose the move that was visited the most (standard MCTS practice)
        best_move = max(root.children, key=lambda c: c.visits).move
        print(f"MCTS Agent chose move: {best_move}")
        return best_move

    def get_result(self, state):
        """
        Determines the result of the simulation from the perspective of this MCTS agent.
        Returns: 1.0 for Win, 0.0 for Loss, 0.5 for Draw.
        """
        winner = self.evaluator.check_global_win(state)

        # Actual win/loss
        if winner == self.player_id:
            return 1.0
        elif winner == -self.player_id:
            return 0.0
        elif not state.get_valid_moves():
            return 0.5  # Draw

        # If the game isn't over but we stopped early (because of Heuristic flag)
        if self.use_heuristic:
            score = self.evaluator.evaluate_board(state)
            # Remember: evaluate_board returns positive for Player 1, negative for Player -1
            if self.player_id == 1:
                if score > 0:
                    return 1.0
                elif score < 0:
                    return 0.0
            else:
                if score < 0:
                    return 1.0
                elif score > 0:
                    return 0.0

        return 0.5  # Default draw if score is exactly 0