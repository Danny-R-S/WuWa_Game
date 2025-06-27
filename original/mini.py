import tkinter as tk

from tkinter import messagebox, simpledialog

import copy

from ai_player import BlackVsWhiteAI


class BlackVsWhiteGame:

    def __init__(self, root):
        
        self.root = root

        self.root.title("Black vs. White Minigame")
        
        self.ai_enabled = False
        self.ai = BlackVsWhiteAI(self)
        
        self.board = {'1': None, '2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, 'C': None}

        self.current_player = 'B'

        self.history = []

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

        self.moves_frame = tk.Frame(self.root)
        
        self.ai_button = tk.Button(self.moves_frame, text="Enable AI", command=self.toggle_ai)
        self.ai_button.pack()

        self.moves_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.status_label = tk.Label(self.moves_frame, text="Black's turn", font=("Arial", 12, "bold"))

        self.status_label.pack()

        self.moves_listbox = tk.Listbox(self.moves_frame, width=20, height=10)

        self.moves_listbox.pack()

        self.undo_button = tk.Button(self.moves_frame, text="Undo Move", command=self.undo_move)

        self.undo_button.pack()

        self.draw_board()



    def draw_board(self):

        self.canvas.delete("all")

        for pos, (x, y) in self.positions.items():

            color = 'black' if self.board[pos] == 'B' else 'white' if self.board[pos] == 'W' else 'lightgray'

            self.canvas.create_oval(x-25, y-25, x+25, y+25, fill=color, outline='black')

            text = pos if pos != 'C' else 'C'

            text_color = 'white' if self.board[pos] == 'B' else 'black'

            self.canvas.create_text(x, y, text=text, font=("Arial", 14), fill=text_color)



    def choose_starting_state(self):

        black_positions = simpledialog.askstring("Input", "Enter Black's starting positions (e.g., C 3 5):", parent=self.root)

        white_positions = simpledialog.askstring("Input", "Enter White's starting positions (e.g., 2 4 7):", parent=self.root)

        if black_positions and white_positions:

            black = black_positions.split()

            white = white_positions.split()

            if len(black) == 3 and len(white) == 3 and all(p in self.board for p in black + white) and len(set(black + white)) == 6:

                for pos in black:

                    self.board[pos] = 'B'

                for pos in white:

                    self.board[pos] = 'W'

                self.update_moves()

                self.draw_board()

            else:

                messagebox.showerror("Error", "Invalid positions. Use 3 unique positions from 1-8 or C, no overlaps.")

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

        return any(all(temp_board[pos] == self.current_player for pos in combo) for combo in self.winning_combos)



    def update_moves(self):

        self.moves_listbox.delete(0, tk.END)

        moves = self.get_available_moves()

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
            move = self.moves_listbox.get(selection[0]).split()
            from_pos, to_pos = move[0], move[2]
            self.history.append((copy.deepcopy(self.board), self.current_player))
            self.board[from_pos] = None
            self.board[to_pos] = self.current_player
            self.draw_board()
            if self.check_winner():
                messagebox.showinfo("Game Over", f"{'Black' if self.current_player == 'B' else 'White'} wins!")
                self.moves_listbox.delete(0, tk.END)
                return
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            self.update_moves()
            if self.ai_enabled and self.current_player == 'W':
                self.root.after(500, self.make_ai_move)
    def check_winner(self):

        return any(all(self.board[pos] == self.current_player for pos in combo) for combo in self.winning_combos)



    def undo_move(self):

        if self.history:

            self.board, self.current_player = self.history.pop()

            self.draw_board()

            self.update_moves()
    def toggle_ai(self):
        self.ai_enabled = not self.ai_enabled
        self.ai_button.config(text="Disable AI" if self.ai_enabled else "Enable AI")
        if self.ai_enabled and self.current_player == 'W':  # Assuming AI plays as White
            self.make_ai_move()

    def make_ai_move(self):
        move = self.ai.get_best_move()
        if move:
            from_pos, to_pos = move
            self.history.append((copy.deepcopy(self.board), self.current_player))
            self.board[from_pos] = None
            self.board[to_pos] = self.current_player
            self.draw_board()
            if self.check_winner():
                messagebox.showinfo("Game Over", f"{'Black' if self.current_player == 'B' else 'White'} wins!")
                self.moves_listbox.delete(0, tk.END)
                return
            self.current_player = 'W' if self.current_player == 'B' else 'B'
            self.update_moves()
            if self.ai_enabled and self.current_player == 'W':
                self.root.after(500, self.make_ai_move)  # Delay for visibility

if __name__ == "__main__":

    root = tk.Tk()

    game = BlackVsWhiteGame(root)

    root.mainloop()
