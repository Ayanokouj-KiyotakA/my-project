import random
import copy
import tkinter as tk
from tkinter import messagebox

# Random ma trận 4x4
initial_state = [[random.randint(0,1) for j in range(4)] for i in range(4)]

model = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
    "SUCK": (0, 0)
}

rules = ["SUCK", "RIGHT", "DOWN", "LEFT", "UP"]

action = None
x, y = 0, 0
current_state = copy.deepcopy(initial_state)

def count_dirty(state):
    return sum(row.count(1) for row in state)

def update_state(state, action, percept, model):
    global x, y

    if action is None:
        return percept

    if action == "SUCK":
        state[x][y] = 0
    else:
        dx, dy = model[action]
        x += dx
        y += dy

    return state

def rule_match(state, rules):
    # Nếu ô hiện tại bẩn
    if state[x][y] == 1:
        return "SUCK"

    # Nếu sạch thì tìm hướng đi hợp lệ
    for rule in rules:
        if rule == "SUCK":
            continue

        dx, dy = model[rule]
        nx = x + dx
        ny = y + dy

        if 0 <= nx < 4 and 0 <= ny < 4:
            return rule

def model_based_reflex_agent(percept):
    global current_state
    global action

    current_state = update_state(current_state, action, percept, model)

    # Goal test
    if count_dirty(current_state) == 0:
        return "STOP"

    rule = rule_match(current_state, rules)

    action = rule

    return action

class VacuumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Máy hút bụi - Model Based Agent (4x4)")
        self.state = copy.deepcopy(initial_state)
        self.x = 0
        self.y = 0
        self.action = None
        self.step_count = 0
        self.running = False
        self.cells = []

        self.build_ui()
        self.update_ui()

    def build_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()

        self.grid_frame = tk.Frame(frame)
        self.grid_frame.grid(row=0, column=0, columnspan=4, pady=(0, 12))

        for i in range(4):
            row_cells = []
            for j in range(4):
                label = tk.Label(
                    self.grid_frame,
                    text="",
                    width=6,
                    height=3,
                    relief="ridge",
                    borderwidth=2,
                    font=("Arial", 12, "bold")
                )
                label.grid(row=i, column=j, padx=1, pady=1)
                row_cells.append(label)
            self.cells.append(row_cells)

        self.status_label = tk.Label(frame, text="", font=("Arial", 10))
        self.status_label.grid(row=1, column=0, columnspan=4, sticky="w")

        self.clean_label = tk.Label(frame, text="", font=("Arial", 10))
        self.clean_label.grid(row=2, column=0, columnspan=4, sticky="w")

        button_frame = tk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=(10, 0))

        tk.Button(button_frame, text="Randomize", command=self.randomize, width=10).grid(row=0, column=0, padx=2)
        tk.Button(button_frame, text="Reset", command=self.reset, width=10).grid(row=0, column=1, padx=2)
        tk.Button(button_frame, text="Step", command=self.step, width=10).grid(row=0, column=2, padx=2)
        tk.Button(button_frame, text="Run Auto", command=self.run_auto, width=10).grid(row=0, column=3, padx=2)
        tk.Button(button_frame, text="Stop", command=self.stop_auto, width=10).grid(row=0, column=4, padx=2)

    def update_ui(self):
        dirty_count = count_dirty(self.state)
        self.status_label.config(text=f"Vị trí: ({self.x}, {self.y})  |  Bụi còn lại: {dirty_count}  |  Action: {self.action}  |  Step: {self.step_count}")
        self.clean_label.config(text="Nhấn Step để thực hiện từng bước hoặc Run Auto để chạy tự động.")

        for i in range(4):
            for j in range(4):
                cell = self.cells[i][j]
                state_val = self.state[i][j]
                if i == self.x and j == self.y:
                    bg = "#4da6ff"
                    fg = "white"
                    text = str(state_val)
                elif state_val == 1:
                    bg = "#d47a45"
                    fg = "white"
                    text = "1"
                else:
                    bg = "#f0f0f0"
                    fg = "black"
                    text = "0"
                cell.config(text=text, bg=bg, fg=fg)

    def randomize(self):
        global initial_state, current_state, action, x, y
        initial_state = [[random.randint(0,1) for j in range(4)] for i in range(4)]
        current_state = copy.deepcopy(initial_state)
        self.state = copy.deepcopy(initial_state)
        x, y = 0, 0
        self.x, self.y = 0, 0
        self.action = None
        self.step_count = 0
        if self.running:
            self.stop_auto()
        self.update_ui()

    def reset(self):
        global current_state, action, x, y
        current_state = copy.deepcopy(initial_state)
        self.state = copy.deepcopy(initial_state)
        x, y = 0, 0
        self.x, self.y = 0, 0
        self.action = None
        self.step_count = 0
        if self.running:
            self.stop_auto()
        self.update_ui()

    def step(self):
        global current_state, action, x, y
        if count_dirty(self.state) == 0:
            messagebox.showinfo("Hoàn thành", "Đã hút sạch toàn bộ bụi!")
            return

        percept = copy.deepcopy(current_state)
        action = model_based_reflex_agent(percept)
        self.state = copy.deepcopy(current_state)
        self.x, self.y = x, y
        self.step_count += 1

        self.update_ui()

        if action == "STOP":
            messagebox.showinfo("Hoàn thành", "Đã hút sạch toàn bộ bụi!")

    def run_auto(self):
        if self.running:
            return
        self.running = True
        self.clean_label.config(text="Đang chạy tự động...")
        self.auto_step()

    def auto_step(self):
        if not self.running:
            return
        if count_dirty(self.state) == 0:
            self.running = False
            self.clean_label.config(text="Hoàn thành! Bụi đã được hút sạch.")
            messagebox.showinfo("Hoàn thành", "Đã hút sạch toàn bộ bụi!")
            return

        self.step()
        self.root.after(300, self.auto_step)

    def stop_auto(self):
        self.running = False
        self.clean_label.config(text="Đã dừng. Bạn có thể tiếp tục với Step hoặc Run Auto.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumApp(root)
    root.mainloop()
