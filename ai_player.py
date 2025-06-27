import random
import pickle
import os
from collections import defaultdict
import numpy as np
import copy

class BlackVsWhiteAI:
    def __init__(self, game, player):
        self.game = game
        self.player = player  # 'B' or 'W'
        self.q_table = defaultdict(lambda: 0.0)
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.q_table_file = f"q_table_{player.lower()}.pkl"
        self.previous_q_values = {}
        self.load_q_table()

    def state_to_key(self, board, player):
        board_tuple = tuple((k, board[k]) for k in sorted(board.keys()))
        return (board_tuple, player)

    def get_action_value(self, state, action):
        return self.q_table[(state, action)]

    def get_best_move(self):
        moves = self.game.get_available_moves()
        if not moves:
            return None

        state = self.state_to_key(self.game.board, self.game.current_player)
        
        if random.random() < self.epsilon:
            return random.choice(moves)
        
        q_values = [(self.get_action_value(state, move), move) for move in moves]
        max_q = max(q_values, key=lambda x: x[0])[0]
        best_moves = [move for q, move in q_values if q == max_q]
        return random.choice(best_moves)

    def update_q_table(self, old_state, action, reward, new_state):
        old_q = self.q_table[(old_state, action)]
        future_moves = self.game.get_available_moves()
        future_q = max([self.get_action_value(new_state, move) for move in future_moves], default=0.0)
        new_q = old_q + self.learning_rate * (reward + self.discount_factor * future_q - old_q)
        self.q_table[(old_state, action)] = new_q

    def train(self, old_board, action, reward, new_board):
        old_state = self.state_to_key(old_board, self.game.current_player)
        new_state = self.state_to_key(new_board, self.game.current_player if self.game.current_player == self.player else ('W' if self.player == 'B' else 'B'))
        self.update_q_table(old_state, action, reward, new_state)

    def save_q_table(self):
        with open(self.q_table_file, 'wb') as f:
            pickle.dump(dict(self.q_table), f)

    def load_q_table(self):
        if os.path.exists(self.q_table_file):
            with open(self.q_table_file, 'rb') as f:
                self.q_table = defaultdict(lambda: 0.0, pickle.load(f))

    def inspect_q_table(self, limit=10):
        print(f"Q-Table for {self.player} (Default AI) (showing up to {limit} entries):")
        total_change = 0.0
        count = 0
        for i, ((state, action), q_value) in enumerate(self.q_table.items()):
            if i >= limit:
                break
            board, player = state
            print(f"State: {dict(board)}, Player: {player}, Action: {action}, Q-Value: {q_value}")
            key = (state, action)
            if key in self.previous_q_values:
                total_change += abs(q_value - self.previous_q_values[key])
                count += 1
            self.previous_q_values[key] = q_value
        avg_change = total_change / count if count > 0 else 0.0
        print(f"Total entries: {len(self.q_table)}, Average Q-Value Change: {avg_change:.6f}")

class SharkAI(BlackVsWhiteAI):
    def __init__(self, game, player):
        super().__init__(game, player)
        self.q_table_file = f"q_table_shark_{player.lower()}.pkl"
        self.previous_q_values = {}
        self.load_q_table()

    def opponent_can_win_next(self, new_board):
        opponent = 'W' if self.player == 'B' else 'B'
        for pos, piece in new_board.items():
            if piece == opponent:
                for next_pos in self.game.connections[pos]:
                    if new_board[next_pos] is None:
                        temp_board = copy.deepcopy(new_board)
                        temp_board[pos] = None
                        temp_board[next_pos] = opponent
                        if any(all(temp_board[p] == opponent for p in combo) for combo in self.game.winning_combos):
                            return True
        return False

    def train(self, old_board, action, reward, new_board):
        if self.opponent_can_win_next(new_board):
            reward = -1.0  # Harsh penalty for allowing opponent to win next
        elif reward == 1.0:
            reward = 2.0  # Stronger reward for winning
        old_state = self.state_to_key(old_board, self.game.current_player)
        new_state = self.state_to_key(new_board, self.game.current_player if self.game.current_player == self.player else ('W' if self.player == 'B' else 'B'))
        self.update_q_table(old_state, action, reward, new_state)

    def inspect_q_table(self, limit=10):
        print(f"Q-Table for {self.player} (Shark AI) (showing up to {limit} entries):")
        total_change = 0.0
        count = 0
        for i, ((state, action), q_value) in enumerate(self.q_table.items()):
            if i >= limit:
                break
            board, player = state
            print(f"State: {dict(board)}, Player: {player}, Action: {action}, Q-Value: {q_value}")
            key = (state, action)
            if key in self.previous_q_values:
                total_change += abs(q_value - self.previous_q_values[key])
                count += 1
            self.previous_q_values[key] = q_value
        avg_change = total_change / count if count > 0 else 0.0
        print(f"Total entries: {len(self.q_table)}, Average Q-Value Change: {avg_change:.6f}")