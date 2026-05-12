import copy
import tkinter as tk
from tkinter import messagebox

initial_state = [
    [1, 2, 3],
    [4, 0, 5],
    [6, 7, 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

model = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1)
}

rules = ["UP", "DOWN", "LEFT", "RIGHT"]

action = None
current_state = copy.deepcopy(initial_state)

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def update_state(state, action, percept, model):
    if action is None:
        return percept

    new_state = copy.deepcopy(state)

    x, y = find_blank(new_state)
    dx, dy = model[action]

    nx = x + dx
    ny = y + dy

    new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]

    return new_state

def rule_match(state, rules):
    x, y = find_blank(state)

    for rule in rules:
        dx, dy = model[rule]

        nx = x + dx
        ny = y + dy

        if 0 <= nx < 3 and 0 <= ny < 3:
            return rule

def model_based_reflex_agent(percept):
    global current_state
    global action

    current_state = update_state(current_state, action, percept, model)

    if current_state == goal_state:
        return "STOP"

    rule = rule_match(current_state, rules)

    action = rule

    return action

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle - Model Based Agent")
        self.state = copy.deepcopy(initial_state)
        self.action = None
        self.step_count = 0
        self.cells = []

        self.build_ui()
        self.update_ui()

    def build_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        self.grid_frame = tk.Frame(frame)
        self.grid_frame.grid(row=0, column=0, columnspan=3, pady=(0, 12))

        for i in range(3):
            row_cells = []
            for j in range(3):
                label = tk.Label(
                    self.grid_frame,
                    text="",
                    width=6,
                    height=3,
                    relief="ridge",
                    borderwidth=2,
                    font=("Arial", 14, "bold")
                )
                label.grid(row=i, column=j, padx=2, pady=2)
                row_cells.append(label)
            self.cells.append(row_cells)

        self.status_label = tk.Label(frame, text="", font=("Arial", 12))
        self.status_label.grid(row=1, column=0, columnspan=3, sticky="w")

        button_frame = tk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))

        tk.Button(button_frame, text="Reset", command=self.reset, width=10).grid(row=0, column=0, padx=4)
        tk.Button(button_frame, text="Step", command=self.step, width=10).grid(row=0, column=1, padx=4)
        tk.Button(button_frame, text="Solve", command=self.solve, width=10).grid(row=0, column=2, padx=4)

    def update_ui(self):
        self.status_label.config(text=f"Step: {self.step_count}  |  Action: {self.action}")

        for i in range(3):
            for j in range(3):
                cell = self.cells[i][j]
                value = self.state[i][j]
                if value == 0:
                    bg = "#f0f0f0"
                    fg = "black"
                    text = ""
                else:
                    bg = "#4da6ff"
                    fg = "white"
                    text = str(value)
                cell.config(text=text, bg=bg, fg=fg)

    def reset(self):
        global current_state, action
        current_state = copy.deepcopy(initial_state)
        self.state = copy.deepcopy(initial_state)
        self.action = None
        self.step_count = 0
        self.update_ui()

    def step(self):
        global current_state, action
        if self.state == goal_state:
            messagebox.showinfo("Hoàn thành", "Đã giải quyết xong puzzle!")
            return

        percept = copy.deepcopy(current_state)
        action = model_based_reflex_agent(percept)
        self.state = copy.deepcopy(current_state)
        self.step_count += 1

        self.update_ui()

        if action == "STOP":
            messagebox.showinfo("Hoàn thành", "Đã giải quyết xong puzzle!")

    def solve(self):
        while self.state != goal_state:
            self.step()
            self.root.update()
            self.root.after(500)

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()
