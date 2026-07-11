import csv
from game_env import UltimateTicTacToe
from minmax_agent import MinimaxAgent
from mcts_agent import MCTSAgent
from rule_base_agent import RuleBasedAgent


def check_global_win(env):
    b = env.macro_board
    for i in range(3):
        if abs(b[i][0] + b[i][1] + b[i][2]) == 3: return b[i][0]
        if abs(b[0][i] + b[1][i] + b[2][i]) == 3: return b[0][i]
    if abs(b[0][0] + b[1][1] + b[2][2]) == 3: return b[0][0]
    if abs(b[0][2] + b[1][1] + b[2][0]) == 3: return b[0][2]
    return 0


def run_matchup(agent1, agent2, agent1_name, agent2_name, num_games=10):
    agent1_wins = 0
    agent2_wins = 0
    draws = 0

    print(f"\nStarting Matchup: {agent1_name} vs {agent2_name}...")

    for i in range(num_games):
        env = UltimateTicTacToe()

        if i % 2 == 0:
            current_x, current_o = agent1, agent2
        else:
            current_x, current_o = agent2, agent1

        current_x.player_id = 1
        current_o.player_id = -1

        game_over = False
        while not game_over:
            valid_moves = env.get_valid_moves()
            if not valid_moves:
                draws += 1
                game_over = True
                continue

            move = current_x.get_best_move(env) if env.current_player == 1 else current_o.get_best_move(env)
            if move: env.make_move(move[0], move[1])

            winner = check_global_win(env)
            if winner != 0:
                if winner == 1:
                    if i % 2 == 0:
                        agent1_wins += 1
                    else:
                        agent2_wins += 1
                else:
                    if i % 2 == 0:
                        agent2_wins += 1
                    else:
                        agent1_wins += 1
                game_over = True
        print(f"  Game {i + 1} finished.")
    return agent1_wins, agent2_wins, draws


def run_all_experiments():
    NUM_GAMES = 100
    results = []

    minimax_args = {"player_id": 1, "depth": 3}

    # 1. Minimax vs Rule-Based
    minimax = MinimaxAgent(**minimax_args)
    rule_based = RuleBasedAgent(player_id=-1)
    w1, w2, d = run_matchup(minimax, rule_based, "Minimax", "Rule-Based", NUM_GAMES)
    results.append(["Minimax", "Rule-Based", w1, w2, d])

    # 2. Pure MCTS vs Heuristic MCTS
    pure_mcts = MCTSAgent(player_id=1, iterations=400, use_heuristic=False)
    heuristic_mcts = MCTSAgent(player_id=-1, iterations=400, use_heuristic=True)
    w1, w2, d = run_matchup(pure_mcts, heuristic_mcts, "Pure MCTS", "Heuristic MCTS", NUM_GAMES)
    results.append(["Pure MCTS", "Heuristic MCTS", w1, w2, d])

    # 3. Minimax vs Heuristic MCTS
    minimax_p1 = MinimaxAgent(**minimax_args)
    heuristic_mcts_p2 = MCTSAgent(player_id=-1, iterations=400, use_heuristic=True)
    w1, w2, d = run_matchup(minimax_p1, heuristic_mcts_p2, "Minimax", "Heuristic MCTS", NUM_GAMES)
    results.append(["Minimax", "Heuristic MCTS", w1, w2, d])

    with open("experiment_results.csv", mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Agent 1", "Agent 2", "A1 Wins", "A2 Wins", "Draws"])
        writer.writerows(results)


if __name__ == "__main__":
    run_all_experiments()
