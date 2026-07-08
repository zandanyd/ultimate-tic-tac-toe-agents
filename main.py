from game_env import UltimateTicTacToe
from minmax_agent import MinimaxAgent


def print_board(env):
    """
    Prints the 9x9 board to the console in a readable format,
    drawing lines to separate the 3x3 macro boards.
    """
    symbols = {1: 'X', -1: 'O', 0: '.'}

    print("\n" + "=" * 23)
    print("  ULTIMATE TIC-TAC-TOE")
    print("=" * 23)

    # Print column numbers
    print("    0 1 2   3 4 5   6 7 8")
    print("  " + "-" * 23)

    for r in range(9):
        # Draw horizontal dividers for macro boards
        if r % 3 == 0 and r != 0:
            print("  " + "-" * 23)

        row_str = f"{r} | "
        for c in range(9):
            # Draw vertical dividers for macro boards
            if c % 3 == 0 and c != 0:
                row_str += "| "
            row_str += symbols[env.board[r][c]] + " "
        print(row_str)
    print("  " + "-" * 23 + "\n")


def print_game_status(env):
    """
    Prints where the current player is allowed to make a move.
    """
    if env.next_macro_row == -1:
        print(">> FREE MOVE: You can play in ANY available small board.")
    else:
        print(
            f">> CONSTRAINED MOVE: You MUST play in the small board at (Row: {env.next_macro_row}, Col: {env.next_macro_col}).")


def play_human_vs_agent():
    env = UltimateTicTacToe()

    # Initialize the Agent as Player -1 (O) with a depth limit of 3
    agent = MinimaxAgent(player_id=-1, depth=3)

    print("Welcome to Ultimate Tic-Tac-Toe!")
    print("You are Player X (1). The Agent is Player O (-1).")

    while True:
        print_board(env)

        # Check if the game has ended
        winner = agent.check_global_win(env)
        if winner != 0:
            winner_symbol = 'X' if winner == 1 else 'O'
            print(f"*** GAME OVER! Player {winner_symbol} wins! ***")
            break

        valid_moves = env.get_valid_moves()
        if not valid_moves:
            print("*** GAME OVER! It's a draw! ***")
            break

        # --- Human's Turn ---
        if env.current_player == 1:
            print("\n--- HUMAN'S TURN (X) ---")
            print_game_status(env)

            # Loop until human enters a valid move
            while True:
                try:
                    move_input = input("Enter your move as 'Row Col' (e.g., '3 4'): ")
                    r, c = map(int, move_input.split())

                    if (r, c) in valid_moves:
                        env.make_move(r, c)
                        break
                    else:
                        print("Invalid move! That cell is either taken or not in the allowed macro board.")
                except ValueError:
                    print("Invalid format! Please enter two numbers separated by a space.")

        # --- Agent's Turn ---
        else:
            print("\n--- AGENT'S TURN (O) ---")
            print_game_status(env)

            # Get the best move from the Minimax algorithm
            best_move = agent.get_best_move(env)
            env.make_move(best_move[0], best_move[1])


if __name__ == "__main__":
    play_human_vs_agent()