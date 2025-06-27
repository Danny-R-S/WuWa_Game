import tkinter as tk
from tkinter import messagebox, simpledialog
import copy
from ai_player import BlackVsWhiteAI, SharkAI

class BlackVsWhitePlay:
    def __init__(self, root):
        self.root = root
        self.root.title("Black vs. White")
        self.board = {'1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, 'C': None}
        self.initial_board = None
        self.initial_first_player = 'B'
        self.current_player = 'B'
        self.history = []
        self.black_wins = 0
        self.white_wins = 0
        self.ai_black_default = BlackVsWhiteAI(self, 'B')
        self.ai_black_shark = SharkAI(self, 'B')
        self.ai_white_default = BlackVsWhiteAI(self, 'W')
        self.ai_white_shark = SharkAI(self, 'W')
        self.ai_side = None  # 'B' or 'W' for AI-controlled side
        self.ai_type = "None"  # "None", "Default", or "Shark"
        self.connections = {
            '1': ['C', '2', '8'], '2': ['C', '1', '3'], '3': ['C', '2', '4'], '4': ['C', '3', '5'],
            '5': ['C', '4', '6'], '6': ['C', '5', '7'], '7': ['C', '6', '8'], '8': ['C', '7', '1'],
            'C': ['1', '2', '3', '4', '5', '6', '7', '8']
        }
        self.winning_combos = [('1', 'C', '5'), ('2', 'C', '6'), ('3', 'C', '7'), ('8', 'C', '4')]
        self.positions = {
            '1': (200, 50), '2': (300, 100), '3': (350, 200), '4': (300, 300),
            '5': (200, 350), '6': (100, 300), '7': (50, 200), '8': (100, 100), 'C': (200, 200)
        }
        self.setup_gui()
        self.choose_starting_state()

    def setup_gui(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg='white')
        self.canvas.pack(side=tk.RIGHT)
        self.controls_frame = tk.Frame(self.root)
        tk.Label(self.controls_frame, text="AI Side and Type:").pack()
        self.ai_var = tk.StringVar(value="None")
        tk.OptionMenu(self.controls_frame, self.ai_var, "None", "Black Default", "Black Shark", "White Default", "White Shark", command=self.update_ai).pack()
        self.inspect_button = tk.Button(self.controls_frame, text="Inspect Q-Table", command=self.inspect_q_table)
        self.inspect_button.pack()
        self.new_game_button = tk.Button(self.controls_frame, text="New Game", command=self.choose_starting_state)
        self.new_game_button.pack()
        self.reset_button = tk.Button(self.controls_frame, text="Reset Board", command=self.reset_to_initial)
        self.reset_button.pack()
        self.undo_button = tk.Button(self.controls_frame, text="Undo Move", command=self.undo_move)
        self.undo_button.pack()
        self.scoreboard_label = tk.Label(self.controls_frame, text="Black: 0 | White: 0", font=("Arial", 12, "bold"))
        self.scoreboard_label.pack()
        self.status_label = tk.Label(self.controls_frame, text="Black's turn", font=("Arial", 12, "bold"))
        self.status_label.pack()
        self.moves_listbox = tk.Listbox(self.controls_frame, width=30, height=10)
        self.moves_listbox.pack()
        self.controls_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for pos, (x, y) in self.positions.items():
            color = 'black' if self.board[pos] == 'B' else 'white' if self.board[pos] == 'W' else 'lightgray'
            self.canvas.create_oval(x-25, y-25, x+25, y+25, fill=color, outline='black')
            text = pos if pos != 'C' else 'C'
            text_color = 'white' if self.board[pos] == 'B' else 'black'
            self.canvas.create_text(x, y, text=text, font=("Arial", 14), fill=text_color)

    def update_scoreboard(self):
        self.scoreboard_label.config(text=f"Black: {self.black_wins} | White: {self.white_wins}")

    def choose_starting_state(self):
        black_positions = simpledialog.askstring("Input", "Enter Black's starting positions (e.g., C 3 5):", parent=self.root)
        white_positions = simpledialog.askstring("Input", "Enter White's starting positions (e.g., 2 4 7):", parent=self.root)
        first_player = simpledialog.askstring("Input", "Who goes first? (B for Black, W for White):", parent=self.root)
        if black_positions and white_positions and first_player:
            black = black_positions.split()
            white = white_positions.split()
            first_player = first_player.upper()
            if (len(black) == 3 and len(white) == 3 and 
                all(p in self.board for p in black + white) and 
                len(set(black + white)) == 6 and 
                first_player in ['B', 'W']):
                self.board = {'1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, 'C': None}
                for pos in black:
                    self.board[pos] = 'B'
                for pos in white:
                    self.board[pos] = 'W'
                self.initial_board = copy.deepcopy(self.board)
                self.initial_first_player = first_player
                self.current_player = first_player
                self.history = []
                self.update_moves()
                self.draw_board()
                if self.ai_side == self.current_player:
                    self.root.after(500, self.make_ai_move)
            else:
                messagebox.showerror("Error", "Invalid input. Use 3 unique positions from 1-8 or C, no overlaps, and 'B' or 'W' for first player.")
                self.choose_starting_state()

    def get_available_moves(self):
        moves = []
        for pos, piece in self.board.items():
            if piece == self.current_player:
                for next_pos in self.connections[pos]:
                    if self.board[next_pos] is None:
                        moves.append((pos, next_pos))
        return moves

    def is_winning_move(self, from_pos, to_pos):
        temp_board = copy.deepcopy(self.board)
        temp_board[from_pos] = None
        temp_board[to_pos] = self.current_player
        return any(all(temp_board[p] == self.current_player for p in combo) for combo in self.winning_combos)

    def check_winner(self):
        return any(all(self.board[pos] == self.current_player for pos in combo) for combo in self.winning_combos)

    def get_current_ai(self):
        if self.ai_side == self.current_player:
            if self.ai_type == "Black Default":
                return self.ai_black_default
            elif self.ai_type == "Black Shark":
                return self.ai_black_shark
            elif self.ai_type == "White Default":
                return self.ai_white_default
            elif self.ai_type == "White Shark":
                return self.ai_white_shark
        return None

    def update_moves(self):
        self.moves_listbox.delete(0, tk.END)
        moves = self.get_available_moves()
        ai = self.get_current_ai()
        if ai:
            state = ai.state_to_key(self.board, self.current_player)
            for from_pos, to_pos in moves:
                q_value = ai.get_action_value(state, (from_pos, to_pos))
                move_text = f"{from_pos} to {to_pos} (Q: {q_value:.3f})"
                self.moves_listbox.insert(tk.END, move_text)
                if self.is_winning_move(from_pos, to_pos):
                    self.moves_listbox.itemconfig(tk.END, {'bg': 'yellow', 'fg': 'black'})
        else:
            for from_pos, to_pos in moves:
                move_text = f"{from_pos} to {to_pos}"
                self.moves_listbox.insert(tk.END, move_text)
                if self.is_winning_move(from_pos, to_pos):
                    self.moves_listbox.itemconfig(tk.END, {'bg': 'yellow', 'fg': 'black'})
        self.moves_listbox.bind('<<ListboxSelect>>', self.on_move_select)
        self.status_label.config(text=f"{'Black' if self.current_player == 'B' else 'White'}'s turn")

    def on_move_select(self, event):
        selection = self.moves_listbox.curselection()
        if selection:
            move_text = self.moves_listbox.get(selection[0])
            move = move_text.split()[0:3:2]  # Extract from_pos and to_pos, ignoring Q-value
            from_pos, to_pos = move[0], move[1]
            old_board = copy.deepcopy(self.board)
            self.history.append((old_board, self.current_player))
            self.board[from_pos] = None
            self.board[to_pos] = self.current_player
            self.draw_board()
            ai = self.get_current_ai()
            if ai:
                reward = 1.0 if self.check_winner() and self.current_player == ai.player else -0.1 if not self.get_available_moves() else 0.0
                ai.train(old_board, (from_pos, to_pos), reward, self.board)
            if self.check_winner():
                if self.current_player == 'B':
                    self.black_wins += 1
                else:
                    self.white_wins += 1
                self.update_scoreboard()
                messagebox.showinfo("Game Over", f"{'Black' if self.current_player == 'B' else 'White'} wins!")
                self.moves_listbox.delete(0, tk.END)
                self.ai_black_default.save_q_table()
                self.ai_black_shark.save_q_table()
                self.ai_white_default.save_q_table()
                self.ai_white_shark.save_q_table()
                return
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            self.update_moves()
            if self.get_current_ai():
                self.root.after(500, self.make_ai_move)

    def undo_move(self):
        if self.history:
            self.board, self.current_player = self.history.pop()
            self.draw_board()
            self.update_moves()
            if self.get_current_ai():
                self.root.after(500, self.make_ai_move)

    def update_ai(self, value):
        self.ai_type = value
        self.ai_side = None
        if value.startswith("Black"):
            self.ai_side = 'B'
        elif value.startswith("White"):
            self.ai_side = 'W'
        self.update_moves()
        if self.get_current_ai():
            self.root.after(500, self.make_ai_move)

    def make_ai_move(self):
        ai = self.get_current_ai()
        if ai:
            move = ai.get_best_move()
            if move:
                from_pos, to_pos = move
                old_board = copy.deepcopy(self.board)
                self.history.append((old_board, self.current_player))
                self.board[from_pos] = None
                self.board[to_pos] = self.current_player
                self.draw_board()
                reward = 1.0 if self.check_winner() and self.current_player == ai.player else -0.1 if not self.get_available_moves() else 0.0
                ai.train(old_board, move, reward, self.board)
                if self.check_winner():
                    if self.current_player == 'B':
                        self.black_wins += 1
                    else:
                        self.white_wins += 1
                    self.update_scoreboard()
                    messagebox.showinfo("Game Over", f"{'Black' if self.current_player == 'B' else 'White'} wins!")
                    self.moves_listbox.delete(0, tk.END)
                    self.ai_black_default.save_q_table()
                    self.ai_black_shark.save_q_table()
                    self.ai_white_default.save_q_table()
                    self.ai_white_shark.save_q_table()
                    return
                self.current_player = 'W' if self.current_player == 'B' else 'B'
                self.update_moves()
                if self.get_current_ai():
                    self.root.after(500, self.make_ai_move)
            self.ai_black_default.save_q_table()
            self.ai_black_shark.save_q_table()
            self.ai_white_default.save_q_table()
            self.ai_white_shark.save_q_table()

    def inspect_q_table(self):
        choice = simpledialog.askstring("Input", "Inspect which Q-Table? (B for Black Default, BS for Black Shark, W for White Default, WS for White Shark):", parent=self.root)
        if choice and choice.upper() in ['B', 'BS', 'W', 'WS']:
            ai = {
                'B': self.ai_black_default,
                'BS': self.ai_black_shark,
                'W': self.ai_white_default,
                'WS': self.ai_white_shark
            }[choice.upper()]
            ai.inspect_q_table()
        else:
            messagebox.showerror("Error", "Invalid choice. Enter 'B', 'BS', 'W', or 'WS'.")

    def reset_to_initial(self):
        if self.initial_board:
            self.board = copy.deepcopy(self.initial_board)
            self.current_player = self.initial_first_player
            self.history = []
            self.draw_board()
            self.update_moves()
            if self.get_current_ai():
                self.root.after(500, self.make_ai_move)

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackVsWhitePlay(root)
    root.mainloop()