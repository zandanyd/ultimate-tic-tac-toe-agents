# ultimate-tic-tac-toe-agents 
<img width="200" height="200" alt="image" src="https://github.com/user-attachments/assets/95db38c9-40db-4f24-b08d-866a4490bc5e" /> <img width="200" height="200" alt="image (1)" src="https://github.com/user-attachments/assets/23a722a9-1acb-4c5f-ac1b-e9e123552454" />

An empirical comparative study of classical and statistical search algorithms in the highly tactical environment of Ultimate Tic-Tac-Toe (UTTT). This repository contains the implementations of adversarial agents—specifically an optimized Iterative Deepening Minimax agent and rollout-truncated Monte Carlo Tree Search (MCTS) variants—alongside a rule-based baseline and a Pygame-driven graphical user interface (GUI) built for human evaluation.



## 🎮 How to Play and Run the Game

The project contains two dedicated entry points depending on the desired game mode. Ensure you have Pygame installed before launching (`pip install pygame`).

### 1. Play Against the Minimax Agent (Singleplayer)
To test your skills against the optimized Iterative Deepening Minimax agent, run the main UI script:
```bash
python UI.py
```
Alternate Start Protocol: To ensure a fair assessment, the starting player alternates automatically with every game based on local match history tracking.
Returning to Menu / Next Game: Once a game concludes, press R to automatically alternate roles and start the next match. Press ESC to exit back to the terminal interface.
2. Local Pass-and-Play (Multiplayer)
To play locally with a friend on the same screen, launch the multiplayer interface:
code
```bash
python multiplayer.py
```
## 🖼️ Graphical User Interface (GUI)
The custom Pygame GUI visually communicates the hierarchical state representation of UTTT, managing both the individual 3×3 micro-grids and the global 3×3 macro-board.

<img width="200" height="200" alt="image (1)" src="https://github.com/user-attachments/assets/1cae2536-9288-444c-8b1b-43ad39e88964" />

## 🤖 Implemented Agents
Iterative Deepening Minimax: Optimized using Alpha-Beta pruning and a Transposition Table (memoization cache) to handle the directed acyclic graph (DAG) structure of the game state. Operating under a strict 2.0-second time limit, it evaluates branches to varying depths depending on branching factor constraints.
Pure MCTS: A statistical sampling agent driven by the standard Upper Confidence bound applied to Trees (UCT) formula. It conducts completely random rollouts to terminal game states to approximate state values.
Heuristic MCTS: Designed to combat MCTS vulnerability to deep tactical traps. Rollouts are truncated at a maximum depth of 15 steps, and non-terminal leaf nodes are evaluated statically using our domain-specific heuristic function.
Deterministic Rule-Based Baseline: Evaluates moves based on a strict priority ladder: local board wins, local board blocks, local center control, and fallback random selections.
## 📊 Empirical Evaluation & Tournament Results
We conducted extensive, fairness-controlled tournaments (alternating starting positions to negate the First-Player Advantage) to establish a comprehensive performance hierarchy.
1. Simulation Matchups (100-Game Tournaments)
The classical, depth-first exhaustive Minimax agent dominated both the rule-based baseline and the statistical sampling frameworks:
Agent 1	Agent 2	Agent 1 Wins	Agent 2 Wins	Draws
Minimax	Rule-Based	94	2	4
Pure MCTS	Heuristic MCTS	44	46	10
Minimax	Heuristic MCTS	74	18	8
The MCTS Equivalence: The dead heat (46 to 44) between Pure MCTS and Heuristic MCTS highlighted that truncating simulations early and mapping continuous evaluations to a flat, binary step-function introduces significant backpropagation noise, neutralizing the benefits of handcrafted domain knowledge.
2. Human Evaluation Tournament (20-Game Tournament)
A 20-game tournament was held against analytical human players under strict time constraints, using a strictly alternated start sequence (10 matches starting as Player 1 for each side):
Minimax (Agent 1)	Human (Agent 2)	Draws
12 (60%)	6 (30%)	2 (10%)
Analysis: Human players managed to bridge the tactical gap by exploiting the strong First-Player Advantage when starting first, and through strategic pattern adaptation (identifying the agent's deterministic preference for local center-cells). However, the agent's absolute tactical safety and lack of blunder vulnerability ultimately secured a 60% majority win rate.
🛠️ Project Structure
code
```bash
├── game_env.py          # Primary Ultimate Tic-Tac-Toe environment logic
├── minmax_agent.py      # Iterative Deepening Minimax agent with transposition caching
├── mcts_agent.py        # Implementation of Pure and Heuristic MCTS agents
├── UI.py                # Graphical interface for Human vs. Agent play
├── multiplayer.py       # Graphical interface for Local Human vs. Human play
├── experiment_results.csv # Local tracking file for tournament and evaluation logs
└── images/              # Visual assets for the documentation

