import tkinter as tk
import heapq
import random
from threading import Thread


def manhattan(puzzle):
    distance = 0
    for i, val in enumerate(puzzle):
        if val == 0:
            continue
        goal_row, goal_col = divmod(val - 1, 4)
        curr_row, curr_col = divmod(i, 4)
        distance += abs(goal_row - curr_row) + abs(goal_col - curr_col)
    return distance


def get_neighbors(state):
    neighbors = []
    idx = state.index(0)
    row, col = divmod(idx, 4)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in moves:
        new_r, new_c = row + dr, col + dc
        if 0 <= new_r < 4 and 0 <= new_c < 4:
            new_idx = new_r * 4 + new_c
            new_state = list(state)
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            neighbors.append(tuple(new_state))
    return neighbors

# A* Algorithm
def a_star(start):
    goal = tuple(range(1, 16)) + (0,)
    open_set = []
    heapq.heappush(open_set, (manhattan(start), 0, start, []))
    visited = set()

    while open_set:
        est_total, cost, curr, path = heapq.heappop(open_set)
        if curr in visited:
            continue
        visited.add(curr)
        if curr == goal:
            return path
        for neighbor in get_neighbors(curr):
            if neighbor not in visited:
                heapq.heappush(open_set, (cost + 1 + manhattan(neighbor), cost + 1, neighbor, path + [neighbor]))
    return None

# GUI Class
class PuzzleGUI:
    def __init__(self, master): 
        self.master = master
        self.master.title("15-Puzzle Solver with A*")
        self.board = list(range(1, 16)) + [0]
        while True:
            random.shuffle(self.board)
            if self.is_solvable(self.board):
                break
        self.buttons = []
        self.draw_board()

        solve_btn = tk.Button(master, text="Solve Puzzle", command=self.solve)
        solve_btn.grid(row=4, column=0, columnspan=4, sticky="nsew")

    def draw_board(self):
        for i in range(16):
            row, col = divmod(i, 4)
            num = self.board[i]
            if len(self.buttons) < 16:
                btn = tk.Button(self.master, text=str(num) if num != 0 else "", width=6, height=3,
                                command=lambda i=i: self.move_tile(i))
                btn.grid(row=row, column=col)
                self.buttons.append(btn)
            else:
                self.buttons[i].config(text=str(num) if num != 0 else "")

    def move_tile(self, i):
        zero = self.board.index(0)
        if abs(zero - i) in (1, 4) and (zero // 4 == i // 4 or zero % 4 == i % 4):
            self.board[zero], self.board[i] = self.board[i], self.board[zero]
            self.draw_board()

    def solve(self):
        def auto():
            path = a_star(tuple(self.board))
            if path:
                for step in path:
                    self.board = list(step)
                    self.draw_board()
                    self.master.update()
                    self.master.after(200)
        Thread(target=auto).start()

    def is_solvable(self, board):
        inv = 0
        for i in range(15):
            for j in range(i + 1, 16):
                if board[i] and board[j] and board[i] > board[j]:
                    inv += 1
        row = board.index(0) // 4
        return (inv + row) % 2 == 0

# Run GUI
if __name__ == "__main__": 
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
