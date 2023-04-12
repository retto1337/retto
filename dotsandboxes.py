import tkinter as tk
from tkinter import messagebox
from copy import deepcopy
import random
import math

class DotsAndBoxes:
    def __init__(self, master):
        self.master = master
        self.master.title('Dots and Boxes')
        self.master.resizable(False, False)

        self.player_turn = random.choice(['Player', 'Computer'])
        self.board_size = 4
        self.score = {'Player': 0, 'Computer': 0}
        self.max_depth = 3

        self.setup_board()

        if self.player_turn == 'Computer':
            self.computer_move()

    def setup_board(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=400, height=400, bg='white')
        self.canvas.pack()

        self.status_label = tk.Label(self.frame, text=f'{self.player_turn} turn', font=('Arial', 14))
        self.status_label.pack()

        self.reset_button = tk.Button(self.frame, text='Reset', command=self.reset_game)
        self.reset_button.pack()

        self.draw_board()

    def draw_board(self):
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.lines = []

        for i in range(self.board_size):
            for j in range(self.board_size):
                x, y = i * 100 + 50, j * 100 + 50
                self.board[i][j] = self.canvas.create_oval(x, y, x + 10, y + 10, fill='black')

        self.canvas.bind('<Button-1>', self.make_move)

    def reset_game(self):
        self.canvas.delete('all')
        self.score = {'Player': 0, 'Computer': 0}
        self.draw_board()
        self.update_status_label()

    def make_move(self, event):
        x, y = event.x, event.y
        i, j = (x - 25) // 100, (y - 25) // 100
        line_added = False

        if 50 <= x % 100 <= 90 and abs(y % 100 - 50) < 10:
            line = self.canvas.create_line(i * 100 + 50, j * 100 + 50, i * 100 + 50, (j + 1) * 100 + 50, fill='blue', width=3)
            if line not in self.lines:
                self.lines.append(line)
                line_added = True

        elif 50 <= y % 100 <= 90 and abs(x % 100 - 50) < 10:
            line = self.canvas.create_line(i * 100 + 50, j * 100 + 50, (i + 1) * 100 + 50, j * 100 + 50, fill='blue', width=3)
            if line not in self.lines:
                self.lines.append(line)
                line_added = True

        if line_added:
            completed_box = self.check_for_completed_boxes(i, j)
            if not completed_box:
                self.switch_turn()
            else:
                self.score[self.player_turn] += 1
                self.update_status_label()

            if self.player_turn == 'Computer':
                self.computer_move()
    def computer_move(self):
        best_score = -math.inf
        best_move = None

        for i in range(self.board_size):
            for j in range(self.board_size):
                for orientation in ['horizontal', 'vertical']:
                    if self.is_valid_move(i, j, orientation) and not self.move_exists(i, j, orientation):
                        new_lines = self.lines.copy()
                        line = self.create_line(i, j, orientation)
                        new_lines.append(line)

                        score = self.minimax(new_lines, 0, False)

                        if score > best_score:
                            best_score = score
                            best_move = (i, j, orientation)

        i, j, orientation = best_move
        line = self.create_line(i, j, orientation, fill='red', width=3)
        self.lines.append(line)
        self.canvas.tag_raise(line)

        completed_box = self.check_for_completed_boxes(i, j)
        if not completed_box:
            self.switch_turn()
        else:
            self.score[self.player_turn] += 1

    def minimax(self, lines, depth, is_maximizing):
        if depth == self.max_depth:
            return self.score['Computer'] - self.score['Player']

        if is_maximizing:
            best_score = -math.inf

            for i in range(self.board_size):
                for j in range(self.board_size):
                    for orientation in ['horizontal', 'vertical']:
                        if self.is_valid_move(i, j, orientation) and not self.move_exists(i, j, orientation, lines):
                            new_lines = lines.copy()
                            line = self.create_line(i, j, orientation)
                            new_lines.append(line)

                            score = self.minimax(new_lines, depth + 1, False)
                            best_score = max(best_score, score)

            return best_score
        else:
            best_score = math.inf

            for i in range(self.board_size):
                for j in range(self.board_size):
                    for orientation in ['horizontal', 'vertical']:
                        if self.is_valid_move(i, j, orientation) and not self.move_exists(i, j, orientation, lines):
                            new_lines = lines.copy()
                            line = self.create_line(i, j, orientation)
                            new_lines.append(line)

                            score = self.minimax(new_lines, depth + 1, True)
                            best_score = min(best_score, score)

            return best_score

    def is_valid_move(self, i, j, orientation):
        if orientation == 'horizontal':
            return i < self.board_size - 1
        else:
            return j < self.board_size - 1

    def move_exists(self, i, j, orientation, lines=None):
        if lines is None:
            lines = self.lines

        line = self.create_line(i, j, orientation)
        return line in lines

    def create_line(self, i, j, orientation, fill=None, width=None):
        if orientation == 'horizontal':
            x1, y1 = i * 100 + 50, j * 100 + 50
            x2, y2 = (i + 1) * 100 + 50, j * 100 + 50
        else:
            x1, y1 = i * 100 + 50, j * 100 + 50
            x2, y2 = i * 100 + 50, (j + 1) * 100 + 50

        if fill and width:
            return self.canvas.create_line(x1, y1, x2, y2, fill=fill, width=width)
        else:
            return (x1, y1, x2, y2)
    def check_for_completed_boxes(self, i, j):
        completed_box = False

        if i < self.board_size - 1 and j < self.board_size - 1:
            if self.move_exists(i, j, 'horizontal') and self.move_exists(i, j, 'vertical') and self.move_exists(i + 1, j, 'vertical') and self.move_exists(i, j + 1, 'horizontal'):
                completed_box = True

        if i > 0 and j < self.board_size - 1:
            if self.move_exists(i - 1, j, 'horizontal') and self.move_exists(i - 1, j, 'vertical') and self.move_exists(i, j, 'vertical') and self.move_exists(i - 1, j + 1, 'horizontal'):
                completed_box = True

        if i < self.board_size - 1 and j > 0:
            if self.move_exists(i, j - 1, 'horizontal') and self.move_exists(i, j - 1, 'vertical') and self.move_exists(i + 1, j - 1, 'vertical') and self.move_exists(i, j, 'horizontal'):
                completed_box = True

        if i > 0 and j > 0:
            if self.move_exists(i - 1, j - 1, 'horizontal') and self.move_exists(i - 1, j - 1, 'vertical') and self.move_exists(i, j - 1, 'vertical') and self.move_exists(i - 1, j, 'horizontal'):
                completed_box = True

        return completed_box

    def switch_turn(self):
        self.player_turn = 'Computer' if self.player_turn == 'Player' else 'Player'
        self.update_status_label()

    def update_status_label(self):
        self.status_label.config(text=f"{self.player_turn}'s turn - Player: {self.score['Player']} | Computer: {self.score['Computer']}")

if __name__ == '__main__':
    root = tk.Tk()
    game = DotsAndBoxes(root)
    root.mainloop()