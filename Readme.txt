Black vs. White Minigame


Author's note at the bottom of page.


Overview
The Black vs. White Minigame is a Python-based game with a graphical user interface (GUI) built using Tkinter. It allows players to play a strategic board game where Black and White pieces move on a circular board with 9 positions (1-8 and a central position C). The goal is to align three pieces in predefined winning combinations. The project includes three scripts for different use cases: a full-featured game (mini.py), a fast simulation tool (simulator.py), and a streamlined player vs. AI mode (play.py). Two AI implementations, BlackVsWhiteAI (Default) and SharkAI (aggressive), use Q-learning to train and play, with separate Q-tables for each.
Scripts

mini.py: The main game with full features, including manual play, AI play, auto-play for training, and debugging tools.
simulator.py: A minimal GUI for running fast simulations to train AIs, with win counters and abort functionality.
play.py: A streamlined GUI for playing against a chosen AI, displaying Q-values for moves.
ai_player.py: Contains the AI logic (BlackVsWhiteAI and SharkAI) with Q-learning and reward structures.

Setup
Requirements

Python 3.8+
Required libraries: tkinter, numpy
Tkinter is included with standard Python installations.
Install numpy: pip install numpy



Installation

Save all scripts (mini.py, simulator.py, play.py, ai_player.py) in the same directory (e.g., C:\Users\YourName\BlackVsWhite).
Ensure Python is installed and numpy is available.
Run any script using: python script_name.py (e.g., python mini.py).

Game Rules

Board: 9 positions (1-8 around a circle, C in the center) connected by predefined paths (e.g., 1 connects to C, 2, 8).
Setup: Each player (Black and White) starts with 3 pieces placed on user-specified positions (e.g., Black: C 3 5, White: 2 4 7).
Moves: Players move one piece to an adjacent empty position per turn.
Winning: A player wins by aligning their three pieces in one of the winning combinations: (1, C, 5), (2, C, 6), (3, C, 7), or (8, C, 4).
First Player: User specifies who moves first (B for Black, W for White).

AI Details

BlackVsWhiteAI (Default):
Q-learning with rewards: +1.0 (win), -0.1 (no moves), 0.0 (neutral).
Q-tables: q_table_b.pkl (Black), q_table_w.pkl (White).


SharkAI:
Aggressive Q-learning with rewards: +2.0 (win), -1.0 (move allows opponent to win next), -0.1 (no moves), 0.0 (neutral).
Q-tables: q_table_shark_b.pkl (Black), q_table_shark_w.pkl (White).


Q-Learning Parameters:
Learning rate: 0.1
Discount factor: 0.9
Epsilon (exploration): 0.1



Script Details
mini.py
The full-featured game for manual play, AI play, and auto-play simulations.
Features

GUI: Board canvas, move listbox with Q-values, buttons (Enable AI, Inspect Q-Table, Auto Play Games, Abort Auto Play, Reset Board, New Board, Undo Move), scoreboard.
AI Selection: Dropdowns to choose AI (None, Default, Shark) for Black and White.
Auto-Play: Run multiple games to train AIs, with debug logging for moves and results.
Q-Table Inspection: View Q-tables (B, BS, W, WS) to monitor AI learning.
First Player: Choose who starts (B or W) when setting positions.
Debugging: Console logs for board resets and auto-play progress.

Usage

Run: python mini.py
Enter starting positions (e.g., Black: C 3 5, White: 2 4 7) and first player (B or W).
Select AI for each side via dropdowns.
Play manually by clicking moves in the listbox, undo moves, reset the board, or start a new game.
Use "Auto Play Games" to run simulations (requires AI for both sides).
Inspect Q-tables to check AI learning progress.

simulator.py
A minimal GUI for fast AI training through simulations.
Features

GUI: Single window with text boxes (Black/White positions, first player, number of simulations), dropdowns for AI selection (None, Default, Shark), and "Run Simulation" button.
Results Window: Shows win counters (Black and White) and "Abort Simulation" button.
No Board Display: Optimizes for speed by skipping GUI updates during simulation.
Debug Logging: Console output for game starts, moves, and results.

Usage

Run: python simulator.py
Enter Black positions, White positions, first player (B or W), number of simulations (e.g., 1000), and select AI for both sides (e.g., Black: Shark, White: Default).
Click "Run Simulation" to start.
Monitor win counters in the results window; click "Abort Simulation" to stop early.
Check console logs for simulation progress.

play.py
A streamlined GUI for playing against a chosen AI, with Q-values for moves.
Features

GUI: Board canvas, move listbox with Q-values (when AI is active), buttons (New Game, Reset Board, Undo Move, Inspect Q-Table), scoreboard.
AI Selection: Single dropdown to choose AI side and type (None, Black Default, Black Shark, White Default, White Shark).
No Auto-Play: Focused on user vs. AI play.
First Player: Choose who starts when setting positions.

Usage

Run: python play.py
Enter starting positions (e.g., Black: C 3 5, White: 2 4 7) and first player (B or W).
Select AI (e.g., "White Shark") via dropdown.
Play by clicking moves in the listbox; AI moves automatically if selected for the current player.
View Q-values for AI moves in the listbox (e.g., 1 to C (Q: 0.123)).
Use "Undo Move", "Reset Board", or "New Game" to control gameplay.
Inspect Q-tables to monitor AI learning.

Q-Table Management

Files: 
Default AI: q_table_b.pkl (Black), q_table_w.pkl (White).
Shark AI: q_table_shark_b.pkl (Black), q_table_shark_w.pkl (White).


Resetting: Delete Q-table files to start AI training from scratch.
Inspection: Use "Inspect Q-Table" in mini.py or play.py to view Q-values (select B, BS, W, or WS).

Troubleshooting

Errors: Ensure numpy is installed and all scripts are in the same directory.
Hangs: Check console logs for stuck games; try different starting positions or reset Q-tables.
Invalid Input: Use 3 unique positions (1-8, C) per side and B/W for first player.
AI Behavior: If Shark AI is too aggressive or Default AI underperforms, inspect Q-tables or adjust starting positions.

Notes

The game requires valid starting positions (no overlaps, exactly 3 pieces per side).
Shark AI is tuned for aggressive play, prioritizing wins and avoiding moves that allow the opponent to win next.
Use simulator.py for bulk AI training, play.py for interactive play, and mini.py for a full-featured experience.
Debug logs in mini.py and simulator.py help diagnose issues; share output for support.





Author's note-
Hey, Danny here! This is an AI Grok and I made to play "The Lifer" minigame in Oakheart Highcourt, Rinascita for Wuthering Waves. At the moment, only the Black Shark and White Default are fully trained. You can load up the "Play.py" and enter the suggested starting positions, which is how it starts in the game, and select "Black Shark" in the dropdown. My AI will pick the best move to do, and whatever the computer in WuWa responds with, you can input into this program as White's move. Then my AI will pick the best move again. The program in WuWa is purposely written to not pick the best move, so you'll win pretty quickly. Anyways, this was just a fun project, and my first time using q tables to teach AI! 