import pygame
import sys
import os
import csv
from game_env import UltimateTicTacToe
from minmax_agent import MinimaxAgent

# --- Configuration ---
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 9
MACRO_CELL_SIZE = WIDTH // 3
CSV_FILENAME = "experiment_results.csv"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (200, 240, 255)  # Light blue for valid macro boards
P1_WIN_COLOR = (220, 220, 255)  # Faint blue for conquered macro board
P2_WIN_COLOR = (255, 220, 220)  # Faint red for conquered macro board
BLUE = (0, 0, 255)  # X color
RED = (255, 0, 0)  # O color


def get_starting_player():
    """Reads the CSV, counts total games played, and alternates starting player."""
    a1_wins, a2_wins, draws = 0, 0, 0

    if os.path.exists(CSV_FILENAME):
        try:
            with open(CSV_FILENAME, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("Agent 1") == "Minimax" and row.get("Agent 2") == "Human":
                        a1_wins = int(row.get("A1 Wins", 0))
                        a2_wins = int(row.get("A2 Wins", 0))
                        draws = int(row.get("Draws", 0))
                        break
        except Exception as e:
            print(f"Error reading CSV: {e}. Defaulting to Human first.")

    total_games = a1_wins + a2_wins + draws
    print(f"Total games played so far: {total_games}")

    # Even number of games -> Human is Player 1 (X) and starts.
    # Odd number of games  -> Agent is Player 1 (X) and starts.
    if total_games % 2 == 0:
        human_player_id = 1
    else:
        human_player_id = -1

    return human_player_id


def record_result(winner, human_player_id, agent_player_id):
    """Updates the experiment_results.csv with the new game outcome."""
    if not os.path.exists(CSV_FILENAME):
        try:
            with open(CSV_FILENAME, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Agent 1", "Agent 2", "A1 Wins", "A2 Wins", "Draws"])
                writer.writerow(["Minimax", "Rule-Based", 94, 2, 4])
                writer.writerow(["Pure MCTS", "Heuristic MCTS", 44, 46, 10])
                writer.writerow(["Minimax", "Heuristic MCTS", 74, 18, 8])
                writer.writerow(["Minimax", "Human", 0, 0, 0])
        except Exception as e:
            print(f"Error creating default CSV: {e}")
            return

    rows = []
    headers = []
    updated = False

    try:
        with open(CSV_FILENAME, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for r in reader:
                rows.append(r)
    except Exception as e:
        print(f"Error reading CSV for updating: {e}")
        return

    try:
        a1_idx = headers.index("Agent 1")
        a2_idx = headers.index("Agent 2")
        a1_wins_idx = headers.index("A1 Wins")
        a2_wins_idx = headers.index("A2 Wins")
        draws_idx = headers.index("Draws")
    except ValueError as e:
        print(f"CSV headers are missing expected columns: {e}")
        return

    for r in rows:
        if r[a1_idx] == "Minimax" and r[a2_idx] == "Human":
            a1_wins = int(r[a1_wins_idx])
            a2_wins = int(r[a2_wins_idx])
            draws = int(r[draws_idx])

            if winner == human_player_id:
                a2_wins += 1
                print("Result recorded: Human (Agent 2) won.")
            elif winner == agent_player_id:
                a1_wins += 1
                print("Result recorded: Minimax (Agent 1) won.")
            else:
                draws += 1
                print("Result recorded: Draw.")

            r[a1_wins_idx] = str(a1_wins)
            r[a2_wins_idx] = str(a2_wins)
            r[draws_idx] = str(draws)
            updated = True
            break

    if not updated:
        new_row = ["Minimax", "Human", "0", "0", "0"]
        if winner == human_player_id:
            new_row[a2_wins_idx] = "1"
        elif winner == agent_player_id:
            new_row[a1_wins_idx] = "1"
        else:
            new_row[draws_idx] = "1"
        rows.append(new_row)

    try:
        with open(CSV_FILENAME, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print("CSV updated and saved successfully.")
    except Exception as e:
        print(f"Error writing to CSV: {e}")


def draw_board(screen, env, game_over=False):
    screen.fill(WHITE)

    # 1. Draw backgrounds (Highlights and Won Boards)
    for r in range(3):
        for c in range(3):
            rect = pygame.Rect(c * MACRO_CELL_SIZE, r * MACRO_CELL_SIZE, MACRO_CELL_SIZE, MACRO_CELL_SIZE)

            if env.macro_board[r][c] == 1:
                pygame.draw.rect(screen, P1_WIN_COLOR, rect)
            elif env.macro_board[r][c] == -1:
                pygame.draw.rect(screen, P2_WIN_COLOR, rect)
            elif (env.next_macro_row == r and env.next_macro_col == c) or env.next_macro_row == -1:
                if env.macro_board[r][c] == 0:
                    pygame.draw.rect(screen, HIGHLIGHT, rect)

    # 2. Draw the grid lines
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), thickness)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)

    # 3. Draw the X's and O's
    font = pygame.font.SysFont(None, int(CELL_SIZE * 0.8))
    for r in range(9):
        for c in range(9):
            symbol = env.board[r][c]
            if symbol != 0:
                text = 'X' if symbol == 1 else 'O'
                color = BLUE if symbol == 1 else RED
                rendered_text = font.render(text, True, color)
                text_rect = rendered_text.get_rect(
                    center=(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(rendered_text, text_rect)

    # 4. Draw Game Over Overlay
    if game_over:
        # Semi-transparent screen tint
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))  # Dark tint
        screen.blit(overlay, (0, 0))

        # Game Over Text
        font_title = pygame.font.SysFont(None, 42)
        title_text = font_title.render("GAME OVER", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 25))
        screen.blit(title_text, title_rect)

        # Instructions Subtext
        font_sub = pygame.font.SysFont(None, 26)
        sub_text = font_sub.render("Press 'R' to play the next game", True, (210, 210, 210))
        sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25))
        screen.blit(sub_text, sub_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    env = UltimateTicTacToe()

    # Determine starting player based on total games recorded in CSV
    human_player_id = get_starting_player()
    agent_player_id = -human_player_id

    # Initialize the Agent with its assigned ID
    agent = MinimaxAgent(player_id=agent_player_id, depth=3)

    # Update caption and print instructions
    if human_player_id == 1:
        pygame.display.set_caption("Ultimate Tic-Tac-Toe (You: X [Blue] vs Agent: O [Red])")
        print("\n--- NEW GAME ---")
        print("You go first! You are 'X' (Blue).")
    else:
        pygame.display.set_caption("Ultimate Tic-Tac-Toe (Agent: X [Blue] vs You: O [Red])")
        print("\n--- NEW GAME ---")
        print("Agent goes first! Agent is 'X' (Blue). You are 'O' (Red).")

    running = True
    game_over = False
    csv_written = False

    # Draw initial blank board
    draw_board(screen, env, game_over)
    pygame.display.flip()

    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Listen for restart key when game is over
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    # Reset variables for a fresh game
                    env = UltimateTicTacToe()
                    human_player_id = get_starting_player()
                    agent_player_id = -human_player_id
                    agent = MinimaxAgent(player_id=agent_player_id, depth=3)
                    game_over = False
                    csv_written = False

                    # Update window title and prints
                    if human_player_id == 1:
                        pygame.display.set_caption("Ultimate Tic-Tac-Toe (You: X [Blue] vs Agent: O [Red])")
                        print("\n--- NEW GAME ---")
                        print("You go first! You are 'X' (Blue).")
                    else:
                        pygame.display.set_caption("Ultimate Tic-Tac-Toe (Agent: X [Blue] vs You: O [Red])")
                        print("\n--- NEW GAME ---")
                        print("Agent goes first! Agent is 'X' (Blue). You are 'O' (Red).")

                    # Draw clean board
                    draw_board(screen, env, game_over)
                    pygame.display.flip()

            # Human Turn (Determined by assigned human_player_id)
            if event.type == pygame.MOUSEBUTTONDOWN and env.current_player == human_player_id and not game_over:
                x, y = event.pos

                # Convert mouse pixel coordinates to grid rows/columns
                c = x // CELL_SIZE
                r = y // CELL_SIZE

                if (r, c) in env.get_valid_moves():
                    env.make_move(r, c)

                    # Check for global win
                    winner = agent.check_global_win(env)
                    if winner != 0 or not env.get_valid_moves():
                        game_over = True
                        winner_name = "You" if winner == human_player_id else "Agent" if winner == agent_player_id else "Draw"
                        symbol_name = 'X' if winner == 1 else 'O'
                        if winner != 0:
                            print(f"*** GAME OVER! Winner: {winner_name} ({symbol_name}) ***")
                        else:
                            print("*** GAME OVER! It's a Draw! ***")

                        if not csv_written:
                            record_result(winner, human_player_id, agent_player_id)
                            csv_written = True

                    draw_board(screen, env, game_over)
                    pygame.display.flip()

        # Agent Turn (Determined by assigned agent_player_id)
        if env.current_player == agent_player_id and not game_over:
            pygame.event.pump()

            best_move = agent.get_best_move(env)
            if best_move:
                env.make_move(best_move[0], best_move[1])

            # Check for global win
            winner = agent.check_global_win(env)
            if winner != 0 or not env.get_valid_moves():
                game_over = True
                winner_name = "You" if winner == human_player_id else "Agent" if winner == agent_player_id else "Draw"
                symbol_name = 'X' if winner == 1 else 'O'
                if winner != 0:
                    print(f"*** GAME OVER! Winner: {winner_name} ({symbol_name}) ***")
                else:
                    print("*** GAME OVER! It's a Draw! ***")

                if not csv_written:
                    record_result(winner, human_player_id, agent_player_id)
                    csv_written = True

            draw_board(screen, env, game_over)
            pygame.display.flip()


if __name__ == "__main__":
    main()