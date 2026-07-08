import pygame
import sys
from game_env import UltimateTicTacToe

# --- Configuration ---
WIDTH, HEIGHT = 600, 600
CELL_SIZE = WIDTH // 9
MACRO_CELL_SIZE = WIDTH // 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (200, 240, 255)  # Light blue for valid macro boards
P1_WIN_COLOR = (220, 220, 255)  # Faint blue for conquered macro board
P2_WIN_COLOR = (255, 220, 220)  # Faint red for conquered macro board
BLUE = (0, 0, 255)  # X color
RED = (255, 0, 0)  # O color


def check_global_win(env):
    """Helper function to check for a global win."""
    b = env.macro_board
    for i in range(3):
        if abs(b[i][0] + b[i][1] + b[i][2]) == 3: return b[i][0]
        if abs(b[0][i] + b[1][i] + b[2][i]) == 3: return b[0][i]
    if abs(b[0][0] + b[1][1] + b[2][2]) == 3: return b[0][0]
    if abs(b[0][2] + b[1][1] + b[2][0]) == 3: return b[0][2]
    return 0


def draw_board(screen, env):
    screen.fill(WHITE)

    # 1. Draw backgrounds (Highlights and Won Boards)
    for r in range(3):
        for c in range(3):
            rect = pygame.Rect(c * MACRO_CELL_SIZE, r * MACRO_CELL_SIZE, MACRO_CELL_SIZE, MACRO_CELL_SIZE)

            # If a player won this macro board
            if env.macro_board[r][c] == 1:
                pygame.draw.rect(screen, P1_WIN_COLOR, rect)
            elif env.macro_board[r][c] == -1:
                pygame.draw.rect(screen, P2_WIN_COLOR, rect)

            # Highlight valid areas for the current turn (only if not already won)
            elif (env.next_macro_row == r and env.next_macro_col == c) or env.next_macro_row == -1:
                if env.macro_board[r][c] == 0:
                    pygame.draw.rect(screen, HIGHLIGHT, rect)

    # 2. Draw the grid lines
    for i in range(10):
        # Thick lines for the 3x3 macro board dividers, thin for the micro cells
        thickness = 4 if i % 3 == 0 else 1

        # Vertical lines
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), thickness)
        # Horizontal lines
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
                # Center the text in the cell
                text_rect = rendered_text.get_rect(
                    center=(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(rendered_text, text_rect)


def play_human_vs_human():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ultimate Tic-Tac-Toe: Human vs Human")

    env = UltimateTicTacToe()

    running = True
    game_over = False

    # Draw initial blank board
    draw_board(screen, env)
    pygame.display.flip()

    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Human Turn (Works for both Player 1 and Player -1)
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos

                # Convert mouse pixel coordinates to grid rows/columns
                c = x // CELL_SIZE
                r = y // CELL_SIZE

                if (r, c) in env.get_valid_moves():
                    env.make_move(r, c)
                    draw_board(screen, env)
                    pygame.display.flip()

                    # Check for global win
                    winner = check_global_win(env)
                    if winner != 0 or not env.get_valid_moves():
                        game_over = True
                        if winner == 1:
                            result_text = "Winner: X"
                        elif winner == -1:
                            result_text = "Winner: O"
                        else:
                            result_text = "Draw!"
                        print(f"*** GAME OVER! {result_text} ***")
                        pygame.display.set_caption(f"Game Over! {result_text}")


if __name__ == "__main__":
    play_human_vs_human()