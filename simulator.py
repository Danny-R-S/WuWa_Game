import tkinter as tk
from tkinter import messagebox
import copy
from ai_player import BlackVsWhiteAI, SharkAI

class BlackVsWhiteSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Black vs. White Simulator")
        self.ai_black_default = BlackVsWhiteAI(self, 'B')
        self.ai_black_shark = SharkAI(self, 'B')
        self.ai_white_default = BlackVsWhiteAI(self, 'W')
        self.ai_white_shark = SharkAI(self, 'W')
        self.board = {'1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, 'C': None}
        self.initial_board = None
        self.initial_first_player = 'B'
        self.current_player = 'B'
        self.black_wins = 0
        self.white_wins = 0
        self.auto_play_active = False
        self.connections = {
            '1': ['C', '2', '8'], '2': ['C', '1', '3'], '3': ['C', '2', '4'], '4': ['C', '3', '5'],
            '5': ['C', '4', '6'], '6': ['C', '5', '7'], '7': ['C', '6', '8'], '8': ['C', '7', '1'],
            'C': ['1', '2', '3', '4', '5', '6', '7', '8']
        }
        self.winning_combos = [('1', 'C', '5'), ('2', 'C', '6'), ('3', 'C', '7'), ('8', 'C', '4')]
        self.setup_gui()

    def setup_gui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        tk.Label(self.main_frame, text="Black Positions (e.g., C 3 5):").pack()
        self.black_positions_entry = tk.Entry(self.main_frame)
        self.black_positions_entry.pack()

        tk.Label(self.main_frame, text="White Positions (e.g., 2 4 7):").pack()
        self.white_positions_entry = tk.Entry(self.main_frame)
        self.white_positions_entry.pack()

        tk.Label(self.main_frame, text="First Player (B or W):").pack()
        self.first_player_entry = tk.Entry(self.main_frame)
        self.first_player_entry.pack()

        tk.Label(self.main_frame, text="Number of Simulations:").pack()
        self.num_simulations_entry = tk.Entry(self.main_frame)
        self.num_simulations_entry.pack()

        tk.Label(self.main_frame, text="Black AI:").pack()
        self.black_ai_var = tk.StringVar(value="None")
        tk.OptionMenu(self.main_frame, self.black_ai_var, "None", "Default", "Shark").pack()

        tk.Label(self.main_frame, text="White AI:").pack()
        self.white_ai_var = tk.StringVar(value="None")
        tk.OptionMenu(self.main_frame, self.white_ai_var, "None", "Default", "Shark").pack()

        self.run_button = tk.Button(self.main_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack(pady=10)

    def get_available_moves(self):
        moves = []
        for pos, piece in self.board.items():
            if piece == self.current_player:
                for next_pos in self.connections[pos]:
                    if self.board[next_pos] is None:
                        moves.append((pos, next_pos))
        return moves

    def check_winner(self):
        return any(all(self.board[pos] == self.current_player for pos in combo) for combo in self.winning_combos)

    def get_current_ai(self):
        if self.current_player == 'B':
            return self.ai_black_default if self.black_ai_var.get() == "Default" else self.ai_black_shark if self.black_ai_var.get() == "Shark" else None
        else:
            return self.ai_white_default if self.white_ai_var.get() == "Default" else self.ai_white_shark if self.white_ai_var.get() == "Shark" else None

    def reset_to_initial(self):
        if self.initial_board:
            self.board = copy.deepcopy(self.initial_board)
            self.current_player = self.initial_first_player

    def run_simulation(self):
        black_positions = self.black_positions_entry.get()
        white_positions = self.white_positions_entry.get()
        first_player = self.first_player_entry.get().upper()
        try:
            num_simulations = int(self.num_simulations_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Number of simulations must be an integer.")
            return

        if not (black_positions and white_positions and first_player and num_simulations > 0):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        black = black_positions.split()
        white = white_positions.split()
        if (len(black) != 3 or len(white) != 3 or 
            not all(p in self.board for p in black + white) or 
            len(set(black + white)) != 6 or 
            first_player not in ['B', 'W']):
            messagebox.showerror("Error", "Invalid input. Use 3 unique positions from 1-8 or C, no overlaps, and 'B' or 'W' for first player.")
            return

        if self.black_ai_var.get() == "None" or self.white_ai_var.get() == "None":
            messagebox.showerror("Error", "Both Black and White must have an AI selected for simulation.")
            return

        self.board = {'1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, 'C': None}
        for pos in black:
            self.board[pos] = 'B'
        for pos in white:
            self.board[pos] = 'W'
        self.initial_board = copy.deepcopy(self.board)
        self.initial_first_player = first_player
        self.current_player = first_player
        self.black_wins = 0
        self.white_wins = 0
        self.auto_play_active = True

        self.main_frame.destroy()
        self.results_window = tk.Toplevel(self.root)
        self.results_window.title("Simulation Results")
        self.results_frame = tk.Frame(self.results_window)
        self.results_frame.pack(padx=10, pady=10)
        self.scoreboard_label = tk.Label(self.results_frame, text="Black: 0 | White: 0", font=("Arial", 12, "bold"))
        self.scoreboard_label.pack()
        self.abort_button = tk.Button(self.results_frame, text="Abort Simulation", command=self.abort_simulation)
        self.abort_button.pack(pady=10)

        self.run_simulation_loop(num_simulations, 0)

    def update_scoreboard(self):
        self.scoreboard_label.config(text=f"Black: {self.black_wins} | White: {self.white_wins}")

    def abort_simulation(self):
        self.auto_play_active = False
        self.ai_black_default.save_q_table()
        self.ai_black_shark.save_q_table()
        self.ai_white_default.save_q_table()
        self.ai_white_shark.save_q_table()
        self.results_window.destroy()
        self.setup_gui()
        messagebox.showinfo("Simulation Aborted", f"Completed {self.black_wins + self.white_wins} games!\nBlack: {self.black_wins} | White: {self.white_wins}")

    def run_simulation_loop(self, total_games, games_played):
        if not self.auto_play_active or games_played >= total_games:
            self.auto_play_active = False
            self.ai_black_default.save_q_table()
            self.ai_black_shark.save_q_table()
            self.ai_white_default.save_q_table()
            self.ai_white_shark.save_q_table()
            self.results_window.destroy()
            self.setup_gui()
            messagebox.showinfo("Simulation Complete", f"Completed {games_played} games!\nBlack: {self.black_wins} | White: {self.white_wins}")
            return
        self.reset_to_initial()
        print(f"Starting game {games_played + 1}/{total_games}")
        self.play_one_game(total_games, games_played)

    def play_one_game(self, total_games, games_played):
        if not self.auto_play_active:
            print("Simulation aborted during game")
            self.run_simulation_loop(total_games, games_played)
            return
        if self.check_winner() or not self.get_available_moves():
            if self.check_winner():
                winner = 'Black' if self.current_player == 'B' else 'White'
                if self.current_player == 'B':
                    self.black_wins += 1
                else:
                    self.white_wins += 1
                self.update_scoreboard()
                print(f"Game {games_played + 1} ended: {winner} wins")
            else:
                print(f"Game {games_played + 1} ended: No moves available")
            self.ai_black_default.save_q_table()
            self.ai_black_shark.save_q_table()
            self.ai_white_default.save_q_table()
            self.ai_white_shark.save_q_table()
            self.root.after(50, lambda: self.run_simulation_loop(total_games, games_played + 1))
            return
        ai = self.get_current_ai()
        if not ai:
            print(f"No AI for {self.current_player} in game {games_played + 1}")
            self.root.after(50, lambda: self.run_simulation_loop(total_games, games_played + 1))
            return
        move = ai.get_best_move()
        if not move:
            print(f"No valid moves for {self.current_player} in game {games_played + 1}")
            self.ai_black_default.save_q_table()
            self.ai_black_shark.save_q_table()
            self.ai_white_default.save_q_table()
            self.ai_white_shark.save_q_table()
            self.root.after(50, lambda: self.run_simulation_loop(total_games, games_played + 1))
            return
        from_pos, to_pos = move
        old_board = copy.deepcopy(self.board)
        self.board[from_pos] = None
        self.board[to_pos] = self.current_player
        reward = 1.0 if self.check_winner() and self.current_player == ai.player else -0.1 if not self.get_available_moves() else 0.0
        ai.train(old_board, move, reward, self.board)
        print(f"Game {games_played + 1}: {self.current_player} moved {from_pos} to {to_pos}, Reward: {reward}")
        if self.check_winner():
            winner = 'Black' if self.current_player == 'B' else 'White'
            if self.current_player == 'B':
                self.black_wins += 1
            else:
                self.white_wins += 1
            self.update_scoreboard()
            print(f"Game {games_played + 1} ended: {winner} wins")
            self.ai_black_default.save_q_table()
            self.ai_black_shark.save_q_table()
            self.ai_white_default.save_q_table()
            self.ai_white_shark.save_q_table()
            self.root.after(50, lambda: self.run_simulation_loop(total_games, games_played + 1))
            return
        self.current_player = 'W' if self.current_player == 'B' else 'B'
        self.root.after(50, lambda: self.play_one_game(total_games, games_played))

if __name__ == "__main__":
    root = tk.Tk()
    simulator = BlackVsWhiteSimulator(root)
    root.mainloop()